import patreon
from hypercorn import config, asyncio
import quart

from config import db, bot, admins, cents, client_id, client_secret, redirect_uri, address
from main import Main

conf = config.Config()
conf.bind = [address]
app = quart.Quart(__name__)
main = Main()

html_template = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>SVTV Bot</title>
</head>
<body>
<script>
location.replace('https://svtv.org');
</script> 
</body>
</html>
'''


@app.route("/ping")
async def ping():
    return {k: v for (k, v) in quart.request.args.items()}, 200


@app.route("/api")
async def not_main_route():
    user_id = quart.request.args.get("state")
    if not user_id:
        main.log('{"ok": False, "err": "invalid URL: where state parameter, a?"}, 401', 'not_main_route', 'INFO')
        return html_template

    oauth_client = patreon.OAuth(client_id, client_secret)
    try:
        tokens = oauth_client.get_tokens(quart.request.args.get("code"), redirect_uri)
    except Exception as e:
        main.log(str(e), "not_main_route")
        main.log('{"ok": False, "err": "invalid client"}, 401', 'not_main_route')
        return html_template
    main.log(f'get_tokens response for user {user_id}: ' + str(tokens), 'not_main_route')
    access_token = tokens.get("access_token")
    if not access_token:
        main.log('{"ok": False, "err": "invalid client"}, 401', 'not_main_route')
        return html_template
    elif user_id[0] == '-' and user_id[1:].isnumeric():
        try:
            if int(user_id[1:]) not in admins:
                raise Exception("User is not bot admin, abort")
            db.insertDB_patreon_helper(access_token, tokens.get("refresh_token"))
            await bot.send_message(int(user_id[1:]),
                                   "Вы установили все необходимые для работы с апи патреона токены, поздравляю!")
            main.log('{"ok": True, "res": "Congratulation, tokens are set"}, 200', 'not_main_route', 'INFO')
            return html_template
        except Exception as e:
            main.log(str(e), "not_main_route")

    if not user_id.isnumeric():
        main.log('"ok": False, "err": "invalid state parameter: {}", 401'.format(user_id), 'not_main_route', 'INFO')
        return html_template

    api_client = patreon.API(access_token)
    user_response = api_client.fetch_user()
    user = user_response.data()
    pledges = user.relationship('pledges')
    main.log(str(pledges), 'not_main_route')
    if not pledges:
        try:
            await bot.send_message(int(user_id), "Извини, но похоже, что ты не являешься нашим патроном.")
        except Exception as e:
            main.log(str(e), 'not_main_route')
        main.log('"ok": False, "err": "{} not patron", 403'.format(user_id), 'not_main_route', 'INFO')
        return html_template

    attributes = pledges[0].json_data.get("attributes")
    if not attributes:
        main.log('attributes not found, wtf', 'not_main_route')
        return html_template
    amount = attributes.get("amount_cents")
    currency = attributes.get("currency")
    if currency not in cents.keys():
        main.log(f'currency {currency} not found', 'not_main_route')
        return html_template
    patron_id = pledges[0].json_data["relationships"]['patron']['data']['id']
    main.log(f'patron: {patron_id} amount: {amount} currency {currency}', 'not_main_route')
    if amount < cents[currency]:
        try:
            await bot.send_message(int(user_id),
                                   f"Похоже, у тебя недостаточный уровень поддержки на Patreon ({amount} центов), "
                                   f"выбери другой.")
        except Exception as e:
            main.log(str(e), 'not_main_route')
        main.log(f'"ok": False, "err": "{user_id} not true patron", 403', 'not_main_route', 'INFO')
        return html_template
    db.insertDB(user_id, int(patron_id), amount << 3 | [x for x, y in enumerate(cents.keys()) if y == currency][0])
    try:
        await bot.send_message(user_id, "Ты — наш патрон, это хорошо! Теперь введи /start для верификации.")
    except Exception as e:
        main.log(str(e), 'not_main_route')
    main.log(f'"ok": True, "res": "Congratulation! {user_id} should come back to bot for getting link", 200',
             'not_main_route', 'INFO')
    return html_template


async def activday(hand=False):

    patreon_tokens = db.selectDB_patreon_helper()
    if not patreon_tokens:
        for x in admins:
            try:
                await bot.send_message(x, """Похоже, в бд бота нет токенов для работы с апи патреона, это хреново.
Отправь /settokens для их добавления""")
            except Exception as e:
                main.log(str(e), 'activday')
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
                except Exception as e:
                    main.log(str(e), "activday")
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
        main.log(f'{id_telegram}: bye-bye', 'gather_pledges', 'INFO')

    return patron_ids


async def run_server():
    await asyncio.serve(app, conf)
