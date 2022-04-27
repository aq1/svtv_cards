from datetime import timedelta, datetime

from aiogram import types, executor
from aiogram.dispatcher import filters, FSMContext
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from markupsafe import escape

from buttons import auth_button, main_menu_keyboard, donate_bot, accept_pay, sub_menu
from config import bot, chat_id, admins, db as DB, dp, cents, msk
from crypto_helper import activday2, convert_from_usd
from main import Main
from patreon_helper import client_id, redirect_uri, activday
from states import State_SVTV

main = Main()


def auth(func):
    async def wrapper(message):
        if message.chat.id not in admins:
            return
        return await func(message)

    return wrapper


@dp.message_handler(state='*', commands='cancel')
# @dp.message_handler(equals='cancel', ignore_case=True, state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Cancelled.')
    else:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Cancelled.')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply(
        f"Здравствуй!\n\nЭто телеграм бот либертарианского СМИ <a href='https://t.me/svtvnews'>SVTV NEWS</a> для сбора пожертвований.\n\n" \
        f"Здесь вы можете оформить единовременный донат или подписку на несколько месяцев.", parse_mode='HTML',
        reply_markup=main_menu_keyboard, disable_web_page_preview=True)


@dp.message_handler(text=['💵 Отправить донат'])
async def send_donate(message: types.Message):
    await message.reply(
        f"Из-за санкционных ограничений, пользователям из России могут быть недоступны зарубежные сервисы по приёму платежей — и наоборот." \
        f"\n\nВот несколько вариантов, как Вы можете помочь нам:", reply_markup=donate_bot())


@dp.message_handler(text=['🔐 Войти в чат'])
async def join_chat(message: types.Message):
    # await message.reply(f"У нас есть чат для наших патронов! Вы можете авторизоваться через Patreon либо через этого бота.\n\nВход в чат возможен только с наличием подписки " \
    # f"«Читатель» и выше.", reply_markup=login_chat(user_id=message.from_user.id))
    user_bot_subs = DB.selectDB_users_bot(info=(message.from_user.id,))
    if user_bot_subs != []:
        await message.reply(
            f"Вы успешно авторизованы. Благодарим за поддержку нашего <a href='https://svtv.org'>СМИ</a>!\n\n"
            f"Воспользуйтесь <a href='{await main.create_link(message.from_user.first_name)}'>этой ссылкой</a> для входа в чат. "
            f"Она действительна 1 час и работает только у патронов.\n\nВы всегда можете снова нажать кнопочку, чтобы получить новую ссылку!",
            parse_mode='HTML')
        return
    value_whitelist = DB.selectDB_whitelist(message.from_user.id)
    user_sum_crypt = DB.selectDB('sum', 'id_telegram', message.from_user.id)
    if user_sum_crypt:
        user_sum = user_sum_crypt >> 3
        user_cur = [y for x, y in enumerate(cents.keys()) if x == user_sum_crypt & 7][0]
    else:
        user_sum, user_cur = 0, "USD"
    if value_whitelist == message.from_user.id:
        status = await bot.get_chat_member(chat_id, message.from_user.id)
        if status['status'] != 'left' and status['status'] != 'kicked':
            await message.reply(f"Вы уже находитесь в чате по особому приглашению!")
        else:
            await message.reply(
                f"У Вас особое приглашение!\n\nВоспользуйтесь <a href='{await main.create_link(message.from_user.first_name)}'>этой ссылкой</a> для входа в чат. "
                f"Она действительна 1 час.\n\nВы всегда можете воспользоваться командой /start, чтобы получить новую ссылку!",
                parse_mode='HTML')
    elif DB.selectDB('id_telegram', 'id_telegram', message.from_user.id) != message.from_user.id or user_sum <= 0:
        auth_button.url = f"https://www.patreon.com/oauth2/authorize?response_type=code&client_id={client_id}" \
                          f"&redirect_uri={redirect_uri}&state={message.from_user.id}" \
                          f"&scope=users+pledges-to-me"
        main_menu = types.InlineKeyboardMarkup(inline_keyboard=[[auth_button]])
        await message.reply(
            f"Здравствуй! Я помогу тебе попасть в закрытый чат для патронов <a href='https://svtv.org'>SVTV NEWS</a>.\n\n"
            f"Но сначала Вы должны авторизоваться по кнопке ниже, чтобы подтвердить свой аккаунт и уровень поддержки нашего <a href='https://svtv.org'>СМИ</a>. Если Вы в России, то " \
            f"оформить подписку можно прямо в боте, оплатив криптовалютой или другим способом!",
            reply_markup=main_menu, parse_mode='HTML')
    elif user_sum >= cents[user_cur]:
        status = await bot.get_chat_member(chat_id, message.from_user.id)
        if status['status'] != 'left' and status['status'] != 'kicked':
            await message.reply(
                f"Вы уже находитесь в чате. Спасибо Вам большое за поддержку нашего <a href='https://svtv.org'>СМИ</a>!",
                parse_mode='HTML')
        else:
            await message.reply(
                f"Вы успешно авторизованы. Благодарим за поддержку нашего <a href='https://svtv.org'>СМИ</a>!\n\n"
                f"Воспользуйтесь <a href='{await main.create_link(message.from_user.first_name)}'>этой ссылкой</a> для входа в чат. "
                f"Она действительна 1 час и работает только у патронов.\n\nВы всегда можете воспользоваться командой /start, чтобы получить новую ссылку!",
                parse_mode='HTML')
    elif user_sum < cents[user_cur]:
        await message.reply(
            "К сожалению, Ваш уровень поддержки недостаточен для доступа к чату. Доступ в чат открывается только при уровне поддержки «Читатель»."
            "\n\nhttp://patreon.com/svtvnews")


@dp.message_handler(text=['💳 Оформить подписку'])
async def join_chat(message: types.Message):
    await message.reply(f"Выберите уровень подписки", reply_markup=sub_menu())


# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
# value_whitelist = DB.selectDB_whitelist(message.from_user.id)
# user_sum_crypt = DB.selectDB('sum', 'id_telegram', message.from_user.id)
# if user_sum_crypt:
#     user_sum = user_sum_crypt >> 3
#     user_cur = [y for x, y in enumerate(cents.keys()) if x == user_sum_crypt & 7][0]
# else:
#     user_sum, user_cur = 0, "USD"
# if value_whitelist == message.from_user.id:
#     status = await bot.get_chat_member(chat_id, message.from_user.id)
#     if status['status'] != 'left' and status['status'] != 'kicked':
#         await message.reply(f"Вы уже находитесь в чате по особому приглашению!")
#     else:
#         await message.reply(f"У Вас особое приглашение!\n\nВоспользуйтесь <a href='{await main.create_link(message.from_user.first_name)}'>этой ссылкой</a> для входа в чат. "
#         f"Она действительна 1 час.\n\nВы всегда можете воспользоваться командой /start, чтобы получить новую ссылку!", parse_mode='HTML')
# elif DB.selectDB('id_telegram', 'id_telegram', message.from_user.id) != message.from_user.id or user_sum <= 0:
#     auth_button.url = f"https://www.patreon.com/oauth2/authorize?response_type=code&client_id={client_id}" \
#                       f"&redirect_uri={redirect_uri}&state={message.from_user.id}" \
#                       f"&scope=users+pledges-to-me"
#     main_menu = types.InlineKeyboardMarkup(inline_keyboard=[[auth_button]])
#     await message.reply(f"Здравствуй! Я помогу тебе попасть в закрытый чат для патронов <a href='https://svtv.org'>SVTV NEWS</a>.\n\n"
#     f"Но сначала Вы должны авторизоваться по кнопке ниже, чтобы подтвердить свой аккаунт и уровень поддержки нашего <a href='https://svtv.org'>СМИ</a>.",
#     reply_markup=main_menu, parse_mode='HTML')
# elif user_sum >= cents[user_cur]:
#     status = await bot.get_chat_member(chat_id, message.from_user.id)
#     if status['status'] != 'left' and status['status'] != 'kicked':
#         await message.reply(f"Вы уже находитесь в чате. Спасибо Вам большое за поддержку нашего <a href='https://svtv.org'>СМИ</a>!", parse_mode='HTML')
#     else:
#         await message.reply(f"Вы успешно авторизованы. Благодарим за поддержку нашего <a href='https://svtv.org'>СМИ</a>!\n\n"
#         f"Воспользуйтесь <a href='{await main.create_link(message.from_user.first_name)}'>этой ссылкой</a> для входа в чат. "
#         f"Она действительна 1 час и работает только у патронов.\n\nВы всегда можете воспользоваться командой /start, чтобы получить новую ссылку!",
#         parse_mode='HTML')
# elif user_sum < cents[user_cur]:
#     await message.reply("К сожалению, Ваш уровень поддержки недостаточен для доступа к чату. Доступ в чат открывается только при уровне поддержки «Читатель»."
#     "\n\nhttp://patreon.com/svtvnews")

@dp.message_handler(content_types=['new_chat_members'])
async def join_user_chat(message: types.Message):
    try:
        print(message.new_chat_members[0])
        value_whitelist = DB.selectDB_whitelist(message.new_chat_members[0].id)
        user_sum_crypt = DB.selectDB('sum', 'id_telegram', message.new_chat_members[0].id)
        if user_sum_crypt:
            user_sum = user_sum_crypt >> 3
            user_cur = [y for x, y in enumerate(cents.keys()) if x == user_sum_crypt & 7][0]
        else:
            user_sum, user_cur = 0, "USD"
        if value_whitelist == message.new_chat_members[0].id:
            await message.reply(
                f"Поприветствуем <a href='tg://user?id={message.new_chat_members[0].id}'>{message.new_chat_members[0].first_name}</a> в нашем уютном чатике!",
                parse_mode='HTML')
        elif DB.selectDB('id_telegram', 'id_telegram', message.new_chat_members[0].id) != message.new_chat_members[
            0].id:
            await bot.kick_chat_member(chat_id, message.new_chat_members[0].id, until_date=timedelta(seconds=60))
            await bot.send_message(chat_id,
                                   f"Кто-то дал ссылку неавторизованному пользователю. Я успешно выгнал незнакомца!")
        elif user_sum < cents[user_cur]:
            await bot.kick_chat_member(chat_id, message.new_chat_members[0].id, until_date=timedelta(seconds=60))
            await bot.send_message(chat_id,
                                   f"Кто-то дал ссылку неавторизованному пользователю. Я успешно выгнал незнакомца!")
        elif user_sum >= cents[user_cur]:
            await message.reply(
                f"Поприветствуем патрона <a href='tg://user?id={message.new_chat_members[0].id}'>{message.new_chat_members[0].first_name}</a> в нашем уютном чатике!",
                parse_mode='HTML')
        elif value_whitelist != message.new_chat_members[0].id:
            await bot.kick_chat_member(chat_id, message.new_chat_members[0].id, until_date=timedelta(seconds=60))
            await bot.send_message(chat_id,
                                   f"Кто-то дал ссылку неавторизованному пользователю. Я успешно выгнал незнакомца!")
    except Exception as e:
        main.log(str(e), 'join_user_chat')


@auth
@dp.message_handler(filters.Text(startswith=['/add']))
async def add_whitelist(message: types.Message):
    try:
        id = message.text.split()[1]
        value = DB.whitelistDB_add(id)
        status = await bot.get_chat_member(chat_id, id)
        if value == True:
            await message.reply(
                f"<a href='tg://user?id={id}'>{escape(status['user']['first_name'])}</a> уже находится в Белом списке!",
                parse_mode='HTML')
            return
        else:
            DB.whitelistDB_add(id)
            await message.reply(
                f"<a href='tg://user?id={id}'>{escape(status['user']['first_name'])}</a> успешно добавлен в Белый список и может получить ссылку на чат!",
                parse_mode='HTML')
    except Exception as e:
        if str(e) == "User not found":
            if value == True:
                await message.reply(f"Юзверь с айдишником {id} уже находится в Белом списке!",
                                    parse_mode='HTML')
            else:
                DB.whitelistDB_add(id)
                await message.reply(
                    f"Юзверь с айдишником {id} успешно добавлен в Белый список и может получить ссылку на чат!",
                    parse_mode='HTML')
        main.log(str(e), 'add_whitelist')


@dp.message_handler(filters.Text(startswith=['/id']))
async def check_id(message: types.Message):
    try:
        await message.reply(message.chat.id)
        await bot.send_message(399010380, f'HUY')
    except Exception as e:
        main.log(str(e), 'check_id')


@auth
@dp.message_handler(filters.Text(startswith=['/rem']))
async def remove_whitelist(message: types.Message):
    try:
        id = message.text.split()[1]
        status = await bot.get_chat_member(chat_id, id)
        value = DB.selectDB_whitelist(id)
        if value == True:
            await message.reply(
                f"<a href='tg://user?id={id}'>{escape(status['user']['first_name'])}</a> не находится в Белом списке! Исключать некого.",
                parse_mode='HTML')
        elif status['status'] != 'left' or status['status'] != 'kicked':
            DB.whitelistDB_remove(id)
            await message.reply(
                f"<a href='tg://user?id={id}'>{escape(status['user']['first_name'])}</a> успешно вынесен из Белого списка!",
                parse_mode='HTML')
            await bot.unban_chat_member(message.chat.id, id)
            await bot.send_message(chat_id,
                                   f"Мне пришлось выгнать <a href='tg://user?id={id}'>{status['user']['first_name']}</a> за отсутствие подписки :(",
                                   parse_mode='HTML')
        else:
            DB.whitelistDB_remove(id)
            await message.reply(
                f"<a href='tg://user?id={id}'>{escape(status['user']['first_name'])}</a> успешно вынесен из Белого списка и кикнут из чата!",
                parse_mode='HTML')
    except Exception as e:
        if str(e) == "User not found":
            if value == True:
                await message.reply(f"Юзверя с айдишником {id} нет в Белом списке! Исключать некого.",
                                    parse_mode='HTML')
            else:
                DB.whitelistDB_remove(id)
                await message.reply(f"Юзверь с айдишником {id} успешно вынесен из Белого списка и кикнут из чата!",
                                    parse_mode='HTML')
        main.log(str(e), 'remove_whitelist')


@auth
@dp.message_handler(commands="settokens")
async def settokens(message: types.Message):
    auth_button.url = f"https://www.patreon.com/oauth2/authorize?response_type=code&client_id={client_id}" \
                      f"&redirect_uri={redirect_uri}&scope=users+pledges-to-me+my-campaign&state=-{message.from_user.id}"
    main_menu = types.InlineKeyboardMarkup(inline_keyboard=[[auth_button]])
    await message.answer("Нажми на кнопку для установки токенов апи патреона. Это безопасно, не бойся...",
                         reply_markup=main_menu)


# @auth
# @dp.message_handler(commands='cancel', state='*')
# async def cancel(message: types.Message, state):
#     await state.finish()
#     await message.answer("Не хотите — как хотите!")

@auth
@dp.message_handler(commands="patron4ek")
async def patron4ek(message: types.Message):
    resp = await message.answer("<i>Проверяю...</i>")
    uids = await activday(hand=True)
    await resp.delete()
    answer = ''
    if uids:
        answer = "\n\nЭтих людишек я выкинул на мороз за отсутствие подписки:\n"
        answer += "\n".join([f'- <a href="tg://user?id={x}">{x}</a>' for x in uids.values()])
    await message.answer("Проверка пройдена" + answer)


@dp.message_handler(state=State_SVTV.summ_donate)
async def svtv_summ_donate(message: types.Message, state: FSMContext):
    try:
        summ = message.text.split()[0]
        print(summ)
        summ = float(summ)
        print(summ)
        print(type(summ))
        await state.update_data(summ=summ)
        await State_SVTV.comm_state.set()
        await bot.send_message(message.chat.id, f"Введите комментарий, максимум 600 символов!")
    except Exception as e:
        if str(e)[:34] == 'could not convert string to float:':
            print('Не число!')
            return
        main.log(str(e), "svtv_summ_donate")


@dp.message_handler(state=State_SVTV.comm_state)
async def svtv_comm_state(message: types.Message, state: FSMContext):
    try:
        comm = message.text[:600]
        info_state = await state.get_data()
        summ = info_state["summ"]
        currency = info_state["currency"]
        converted_amount = "%f" % convert_from_usd(summ, currency)
        await state.update_data(comment=comm)
        await bot.send_message(message.chat.id,
                               f"<strong>{datetime.strftime(datetime.now(msk), '%d.%m.%Y %H:%M')}</strong>\n\n" \
                               f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>" \
                               f", Вы уверены, что хотите пожертвовать <strong>{summ}$ ({converted_amount} {currency})</strong> со следующим комментарием:\n\n«{comm}»?",
                               reply_markup=accept_pay(summ, currency), parse_mode='HTML')
    except Exception as e:
        if str(e)[:34] == 'could not convert string to float:':
            print('Не число!')
            return await message.answer("Вы ввели что угодно, но только не число, попробуйте снова.")
        main.log(str(e), "svtv_comm_state")


async def set_commands():
    await dp.bot.set_my_commands(commands=[BotCommand('start', 'Старт')], scope=BotCommandScopeAllPrivateChats())


async def on_startup(dp):
    try:
        await set_commands()
        scheduler = AsyncIOScheduler(timezone=msk)
        scheduler.add_job(activday, "cron", hour="12", minute="0", day="1")
        scheduler.add_job(activday2, "cron", hour="13", minute="0",
                          day="1")  # для проверки и исключения тех, кто оформлял подписку в боте
        scheduler.start()
    except Exception as e:
        main.log(str(e), 'on_startup')


if __name__ == '__main__':
    DB.setupDB()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
