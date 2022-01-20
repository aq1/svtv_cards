import patreon
import quart
from hypercorn import config, asyncio

from config import db, bot, admins, cents, client_id, client_secret, redirect_uri, address
from main import Main

conf = config.Config()
conf.bind = [address]
app = quart.Quart(__name__)
main = Main()


@app.route("/ping")
async def ping():
    return {'ping': 'pong'}, 200


@app.route("/patreon/ping")
async def ping1():
    return {'ping': 'patreon pong'}, 200


@app.route("/webhook/patreon/ping")
async def ping2():
    return {'ping': 'webhook pong'}, 200


@app.route("/api")
async def not_main_route():
    user_id = quart.request.args.get("state")
    if not user_id:
        return {"ok": False, "err": "invalid URL: where state parameter, a?"}, 401

    oauth_client = patreon.OAuth(client_id, client_secret)
    try:
        tokens = oauth_client.get_tokens(quart.request.args.get("code"), redirect_uri)
    except Exception as e:
        main.log(str(e), "not_main_route")
        return {"ok": False, "err": "invalid client"}, 401
    access_token = tokens.get("access_token")
    if not access_token:
        # print(str(tokens), str(quart.request.args))
        return {"ok": False, "err": "invalid client"}, 401
    elif user_id[0] == '-' and user_id[1:].isnumeric():
        try:
            if int(user_id[1:]) not in admins:
                raise Exception("User is not bot admin, abort")
            db.insertDB_patreon_helper(access_token, tokens.get("refresh_token"))
            await bot.send_message(int(user_id[1:]),
                                   "Вы установили все необходимые для работы с апи патреона токены, поздравляю!")
            return {"ok": True, "res": "Congratulation, tokens are set"}, 200
        except Exception as e:
            main.log(str(e), "not_main_route")

    if not user_id.isnumeric():
        return {"ok": False, "err": "invalid state parameter"}, 401

    api_client = patreon.API(access_token)
    user_response = api_client.fetch_user()
    # print(str(user_response.json_data), access_token)
    user = user_response.data()
    pledges = user.relationship('pledges')
    # print(str(pledges))
    if not pledges:
        try:
            await bot.send_message(int(user_id), "Извини, но похоже, что ты не являешься нашим патроном.")
        except:
            pass
        return {"ok": False, "err": "You are not patron"}, 403

    for pledge in pledges:
        attributes = pledge.json_data.get("attributes")
        if not attributes:
            return {"ok": False, "err": "wtf"}, 404
        amount = attributes.get("amount_cents")
        if amount <= cents:
            try:
                await bot.send_message(int(user_id),
                                       "Похоже, у тебя недостаточный уровень поддержки на Patreon, выбери другой.")
            except:
                pass
            return {"ok": False, "err": "You are not patron"}, 403
        patron_id = pledge.json_data["relationships"]['patron']['data']['id']
        db.insertDB(user_id, int(patron_id), amount)
        try:
            await bot.send_message(user_id, "Ты — наш патрон, это хорошо! Теперь введи /start для верификации.")
        except:
            pass
        return {"ok": True, "res": "Congratulation! come back to our bot for getting chat link"}, 200

    try:
        await bot.send_message(int(user_id), "Извини, но похоже, что ты не являешься нашим патроном.")
    except:
        pass
    return {"ok": False, "err": "You are not patron"}, 403


async def activday(hand=False):
    # main.log("activday started", "activday")

    patreon_tokens = db.selectDB_patreon_helper()
    if not patreon_tokens:
        for x in admins:
            try:
                await bot.send_message(x, """Похоже, в бд бота нет токенов для работы с апи патреона, это хреново.
Отправь /settokens для их добавления""")
            except:
                continue
        return

    uids = db.selectDB_patreons()
    if not uids:
        return

    access_token = patreon_tokens[0][0]

    try:
        ret = await gather_pledges(access_token, uids)
    except Exception as e:
        main.log(str(e), "activday")
        try:
            oauth_client = patreon.OAuth(client_id, client_secret)
            new_tokens = oauth_client.refresh_token(patreon_tokens[0][1])
            access_token = new_tokens.get("access_token")
            if not access_token:
                raise Exception("invalid refresh token or client credentials")
            db.insertDB_patreon_helper(access_token, new_tokens.get("refresh_token"))
            ret = await gather_pledges(access_token, uids)
        except Exception as e:
            main.log(str(e), "activday")
            for x in admins:
                try:
                    await bot.send_message(x, """Похоже, в бд бота совсем нет рабочих токенов для апи патреона.
Отправь /settokens для их добавления""")
                except:
                    continue
            return

    if hand:
        return ret


async def gather_pledges(access_token, uids):
    api_client = patreon.API(access_token)

    # Get the campaign ID
    campaign_response = api_client.fetch_campaign()
    campaign_id = campaign_response.data()[0].id()

    # Fetch all pledges
    all_pledges = []
    cursor = None
    while True:
        pledges_response = api_client.fetch_page_of_pledges(campaign_id=campaign_id, page_size=25, cursor=cursor)
        all_pledges += pledges_response.data()
        cursor = api_client.extract_cursor(pledges_response)
        if not cursor:
            break

    patron_ids = {x: y for x, y in uids}
    for pledge in all_pledges:
        patron_id = pledge.relationships()['patron']['data']['id']
        if patron_id.isnumeric() and int(patron_id) in patron_ids:
            del patron_ids[int(patron_id)]

    for id_telegram in patron_ids.values():
        db.deleteDB(id_telegram)
        await main.kick(id_telegram)

    return patron_ids


async def run_server():
    await asyncio.serve(app, conf)
