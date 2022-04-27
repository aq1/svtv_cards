from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup

from DBworker import DB
from config import bot, db as DB, dp, msk
from crypto_helper import convert_from_usd, check_transaction
from states import State_SVTV

DB = DB()

auth_button = InlineKeyboardButton("Авторизоваться через Patreon", url='telegra.ph')

donate = KeyboardButton("💵 Отправить донат")
buy_sub = KeyboardButton("💳 Оформить подписку")
# login_in_patreon = KeyboardButton("🚪 Войти через Patreon")
join_to_chat = KeyboardButton("🔐 Войти в чат")

main_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_keyboard.add(donate, buy_sub).add(join_to_chat)


def login_chat(user_id):
    client_id = 1
    redirect_uri = "hufsy"
    print(user_id)
    login_menu = InlineKeyboardMarkup()
    login_in_patreon = InlineKeyboardButton("Войти через Patreon",
                                            url=f"https://www.patreon.com/oauth2/authorize?response_type=code&client_id={client_id}" \
                                                f"&redirect_uri={redirect_uri}&state={user_id}" \
                                                f"&scope=users+pledges-to-me")
    login_in_bot = InlineKeyboardButton("Войти через подписку бота", callback_data='login_in_bot')
    login_menu.add(login_in_patreon).add(login_in_bot)
    return login_menu


def donate_bot():
    donate_menu = InlineKeyboardMarkup()
    yu_kassa = InlineKeyboardButton("🇷🇺 ЮKassa", url='telegra.ph')
    smart_glocal = InlineKeyboardButton("Smart Gloсal", url='telegra.ph')
    crypts = InlineKeyboardButton("Пожертвование в криптовалюте", callback_data='crypts')
    donate_menu.add(yu_kassa).add(smart_glocal).add(crypts)
    return donate_menu


def donate_crypto():
    donate_crypto_menu = InlineKeyboardMarkup()
    donate_with_comm = InlineKeyboardButton("Донат с комментарием", callback_data='donate_with_comm')
    donate_without_comm = InlineKeyboardButton("Обычный донат", callback_data='donate_without_comm')
    donate_crypto_menu.add(donate_without_comm).row(donate_with_comm)
    return donate_crypto_menu


def crypto_menu():
    crypto_inline_menu = InlineKeyboardMarkup()
    v_btc = InlineKeyboardButton("BTC", callback_data='v_btc')
    # v_eth = InlineKeyboardButton("ETH", callback_data='v_eth')
    crypto_inline_menu.add(v_btc)
    return crypto_inline_menu


def crypto_sub_menu(lvl, sub):
    crypto_inline_sub_menu = InlineKeyboardMarkup()
    vs_btc = InlineKeyboardButton("BTC", callback_data=f'vs_btc-{lvl}-{sub}')
    # v_eth = InlineKeyboardButton("ETH", callback_data='v_eth')
    crypto_inline_sub_menu.add(vs_btc)
    return crypto_inline_sub_menu


def accept_pay(summ, currency):
    accept_pay_menu = InlineKeyboardMarkup()
    yes_apm = InlineKeyboardButton("Да", callback_data=f'yes_apm-{summ}-{currency}')
    no_apm = InlineKeyboardButton("Нет", callback_data=f'no_apm-{summ}-{currency}')
    accept_pay_menu.add(yes_apm).row(no_apm)
    return accept_pay_menu


def accept_sub(lvl, dat, currency):
    accept_sub_menu = InlineKeyboardMarkup()
    yes_asm = InlineKeyboardButton("Да", callback_data=f'yes_asm-{lvl}-{dat}-{currency}')
    no_asm = InlineKeyboardButton("Нет", callback_data=f'no_asm-{lvl}-{dat}-{currency}')
    accept_sub_menu.add(yes_asm).row(no_asm)
    return accept_sub_menu


def sub_menu():
    sub_inlinemenu = InlineKeyboardMarkup()
    reader = InlineKeyboardButton("Читатель: 20$ в месяц", callback_data=f'reader')
    reg_reader = InlineKeyboardButton("Постоянный читатель: 50$ в месяц", callback_data='reg_reader')
    sponsor = InlineKeyboardButton("Спонсор: 250$ в месяц", callback_data='sponsor')
    sub_inlinemenu.add(reader).row(reg_reader).row(sponsor)
    return sub_inlinemenu


def sub_period(lvl):
    sub_period_menu = InlineKeyboardMarkup()
    one_month = InlineKeyboardButton("1 месяц", callback_data=f'one_month-{lvl}')
    three_month = InlineKeyboardButton("3 месяца", callback_data=f'three_month-{lvl}')
    six_month = InlineKeyboardButton("6 месяцев", callback_data=f'six_month-{lvl}')
    twelve_month = InlineKeyboardButton("12 месяцев", callback_data=f'twelve_month-{lvl}')
    back_sub = InlineKeyboardButton("назад", callback_data='back_sub')
    sub_period_menu.add(one_month).row(three_month).row(six_month).row(twelve_month).row(back_sub)
    return sub_period_menu


@dp.callback_query_handler(lambda c: True, state='*')
async def inline_handler(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'crypts':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f"Выберите вид доната.\n\nДонат с комментарием позволяет Вам задать вопрос в эфир <a href='https://www.youtube.com/c/SVTVofficial'>канала SVTV</a>.\n\nОбычный донат " \
                                         f"позволяет без лишних слов поддержать либертарианское СМИ — <a href='https://t.me/svtvnews'>SVTV NEWS</a>.",
                                    parse_mode='HTML', disable_web_page_preview=True, reply_markup=donate_crypto())
    elif call.data == 'donate_without_comm':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f"Вот список наших криптокошельков:\n\n<strong>Bitcoin (BTC):</strong>\n<code>1EahjiPKXyAFRbTC9HYL67TMQjZZgfFw9g</code>\n" \
                                         f"<strong>Litecoin (LTC):</strong>\n<code>LTwfHhGa7bQfXhPY7hn7Y1ajhcGMrpcD2N</code>\n" \
                                         f"<strong>Bitcoin Cash (BCH):</strong>\n<code>qzk27dg92j6hfftx7hfa6jyyy60ylsutdg2hgz28na</code>\n" \
                                         f"<strong>DASH:</strong>\n<code>XtqFqLi8VJV7eJ1s98MLbNmSNdZ81vbNVt</code>\n" \
                                         f"<strong>Ethereum (ETH):</strong>\n<code>0x19330e83c2059Ad5B67b8431dd6ba4BD848dec67</code>\n" \
                                         f"<strong>TON:</strong>\n<code>EQCWz0h6Q63UdJFcMUnwrgLM8D6cYOutxISn4NGDnqyrQUq8</code>\n" \
                                         f"<strong>NEO:</strong>\n<code>AdvX9JeJepvesyKyte7bSiPf6BrgENwRHD</code>\n" \
                                         f"<strong>Zcash (ZEC):</strong>\n<code>t1WuCvNNDsRNWaR4rrRjFia2N7SfpPoQYsu</code>\n" \
                                         f"<strong>Monero (XMR):</strong>\n<code>48ruTzXESqg6dBesQpHvJXHeAYVobsDhKa8m4CMgvtBdHTa3mWCFgD7WXpwMXt8TbBSLaN8J1PWtbZNu8WzSxvTiDGMpu8X</code>\n" \
                                         f"<strong>Doge:</strong>\n<code>DFvtMQKNrjWw6xDhD23Pr1cYZTWpPQ7bUo</code>",
                                    parse_mode='HTML')
    elif call.data == 'donate_with_comm':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f"Выберите криптовалюту, в которой вы хотите задонатить.",
                                    reply_markup=crypto_menu())
    elif call.data == 'v_btc':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f"Введите сумму доната в $.\n\nМинимальная сумма — 0.70$\nОтменить операцию — <code>/cancel</code> ",
                                    parse_mode='HTML')
        await state.update_data(id_user=call.from_user.id, currency='BTC')
        await State_SVTV.summ_donate.set()
    elif call.data.split('-')[0] == 'yes_apm':
        try:
            user_state = await dp.storage.get_data(chat=call.from_user.id, user=call.from_user.id)
            if user_state:
                comm = user_state["comment"]
            else:
                comm = ''
            await call.message.delete_reply_markup()
            summ = call.data.split('-')[1]
            currency = call.data.split('-')[2]
            converted_amount = convert_from_usd(float(summ), currency)
            print(currency)
            DB_data = DB.selectDB_wallets(info=(0, currency))
            print(DB_data[0][1])
            DB_data2 = DB.selectDB_check_wallets(info=(call.from_user.id,))
            if DB_data2 != []:
                await bot.send_message(call.message.chat.id, f"Вы уже оформляете платёж!")
                return
            DB.updateDB_wallets(info=(1, call.from_user.id, DB_data[0][1]))
            await bot.send_message(call.message.chat.id,
                                   f"<strong>{datetime.strftime(datetime.now(msk), '%d.%m.%Y %H:%M')}</strong>\n\n" \
                                   f"<a href='tg://user?id={call.from_user.id}'>{call.from_user.first_name}</a>" \
                                   f", в течение 30 минут Вы должны отправить <code>{converted_amount}</code> {currency} на следующий BTC-адрес:\n\n<code>{DB_data[0][1]}</code>" \
                                   f"\n\nТранзакции поступают в сеть примерно раз в 10 минут. Как только мы увидим, что Ваш платёж дошёл — мы сразу же отправим Вам сообщение.",
                                   parse_mode='HTML')
            dp.loop.create_task(
                check_transaction(DB_data[0][1], call.from_user.id, converted_amount, currency, comment=comm))
        except Exception as e:
            print(e)
            if str(e) == 'list index out of range':
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text=f"К сожалению, в данный момент слишком много желающих отправить донат или приобрести подписку. Попробуйте через несколько минут.")
    elif call.data.split('-')[0] == 'no_apm':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f"Нет так нет!. Платёж отменён.")
    elif call.data == 'reader':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f"<strong>Добавим в закрытый чат редакции.</strong>\nСможете лично сказать СММщику, что его шутки несмешные!\n\nНаграды за подписку:\n\n1. " \
                                         f"Благодарность от нас\n2. Закрытый чат в Telegram\n\nВыберете период подписки:",
                                    reply_markup=sub_period(1))
    elif call.data == 'reg_reader':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="<strong>Доступ к каналу с материалами, которые ещё не вышли в свет.</strong>\n\n«Тесты», «Треды», «Мнения» — всё это вы сможете опробовать и оценить раньше других.\n" \
                                         f"Отдельный чат для обсуждения прилагается!\n\nВы получите:\n\n1. Благодарность от нас;\n2. Ранний доступ + Отдельный чат;\n3. Закрытый чат в Telegram." \
                                         f"\n\nВыберете период подписки:", reply_markup=sub_period(2))
    elif call.data == 'sponsor':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="<strong>Сделаем «Тест» по Вашей теме!</strong>\n\nВы получите:\n\n1. Благодарность от нас;\n2. Ранний доступ + Отдельный чат;\n3. Пост по вашей теме;\n4. «Тест» по Вашей теме;"
                                         f"\n5. Закрытый чат в Telegram." \
                                         f"\n\nВыберете период подписки:", reply_markup=sub_period(3))
    elif call.data == 'back_sub':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f"Выберите уровень подписки", reply_markup=sub_menu())
    elif call.data.split('-')[0] == 'vs_btc':
        lvl = call.data.split('-')[1]
        dat = call.data.split('-')[2]
        if lvl == '1':
            name_sub = '«Читатель»'
            summ = 20
        elif lvl == '2':
            name_sub = '«Постоянный читатель»'
            summ = 50
        elif lvl == '3':
            name_sub = '«Спонсор»'
            summ = 250
        if dat == '1':
            dat_text = '1 месяц'
        elif dat == '3':
            dat_text = '3 месяца'
        elif dat == '6':
            dat_text = '6 месяцев'
        elif dat == '12':
            dat_text = '12 месяцев'
        converted_amount = convert_from_usd(summ, 'BTC')
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f"Вы уверены, что хотите оформить подписку {name_sub} на {dat_text} за <strong>{summ}$ ({converted_amount} BTC)?</strong>",
                                    reply_markup=accept_sub(lvl, dat, 'BTC'),
                                    parse_mode='HTML')
    elif call.data.split('-')[0] == 'one_month':
        lvl = call.data.split('-')[1]
        dat = 1
        print(lvl)
        if lvl == '1':
            name_sub = '«Читатель»'
        elif lvl == '2':
            name_sub = '«Постоянный читатель»'
        elif lvl == '3':
            name_sub = '«Спонсор»'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f"Выберете способ оплаты подписки {name_sub} на 1 месяц.",
                                    reply_markup=crypto_sub_menu(lvl, dat))
    elif call.data.split('-')[0] == 'three_month':
        lvl = call.data.split('-')[1]
        dat = 3
        print(lvl)
        if lvl == '1':
            name_sub = '«Читатель»'
        elif lvl == '2':
            name_sub = '«Постоянный читатель»'
        elif lvl == '3':
            name_sub = '«Спонсор»'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f"Выберете способ оплаты подписки {name_sub} на 3 месяца.",
                                    reply_markup=crypto_sub_menu(lvl, dat))
    elif call.data.split('-')[0] == 'six_month':
        lvl = call.data.split('-')[1]
        dat = 6
        print(lvl)
        if lvl == '1':
            name_sub = '«Читатель»'
        elif lvl == '2':
            name_sub = '«Постоянный читатель»'
        elif lvl == '3':
            name_sub = '«Спонсор»'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f"Выберете способ оплаты подписки {name_sub} на 6 месяцев.",
                                    reply_markup=crypto_sub_menu(lvl, dat))
    elif call.data.split('-')[0] == 'twelve_month':
        lvl = call.data.split('-')[1]
        dat = 12
        print(lvl)
        if lvl == '1':
            name_sub = '«Читатель»'
        elif lvl == '2':
            name_sub = '«Постоянный читатель»'
        elif lvl == '3':
            name_sub = '«Спонсор»'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f"Выберете способ оплаты подписки {name_sub} на 12 месяцев.",
                                    reply_markup=crypto_sub_menu(lvl, dat))
    elif call.data.split('-')[0] == 'yes_asm':
        try:
            lvl = call.data.split('-')[1]
            dat = call.data.split('-')[2]
            await call.message.delete_reply_markup()
            if lvl == '1':
                name_sub = '«Читатель»'
                summ = 20
            elif lvl == '2':
                name_sub = '«Постоянный читатель»'
                summ = 50
            elif lvl == '3':
                name_sub = '«Спонсор»'
                summ = 250
            if dat == '1':
                dat_text = '1 месяц'
            elif dat == '3':
                dat_text = '3 месяца'
            elif dat == '6':
                dat_text = '6 месяцев'
            elif dat == '12':
                dat_text = '12 месяцев'
            currency = call.data.split('-')[3]
            converted_amount = convert_from_usd(summ, 'BTC')
            DB_data = DB.selectDB_wallets(info=(0, currency))
            DB_data2 = DB.selectDB_check_wallets(info=(call.from_user.id,))
            if DB_data2 != []:
                await bot.send_message(call.message.chat.id, f"Вы уже оформляете платёж!")
                return
            DB.updateDB_wallets(info=(1, call.from_user.id, DB_data[0][1]))
            await bot.send_message(call.message.chat.id,
                                   f"<strong>{datetime.strftime(datetime.now(msk), '%d.%m.%Y %H:%M')}</strong>\n\n" \
                                   f"Оформление подписки {name_sub} на {dat_text}.\n\n"
                                   f"<a href='tg://user?id={call.from_user.id}'>{call.from_user.first_name}</a>" \
                                   f", в течение 30 минут Вы должны отправить <code>{converted_amount}</code> {currency} на следующий BTC-адрес:\n\n<code>{DB_data[0][1]}</code>" \
                                   f"\n\nТранзакции поступают в сеть примерно раз в 10 минут. Как только мы увидим, что Ваш платёж дошёл — мы сразу же отправим Вам сообщение.",
                                   parse_mode='HTML')
            dp.loop.create_task(
                check_transaction(DB_data[0][1], call.from_user.id, converted_amount, currency, name_sub, dat))
        except Exception as e:
            print(e)
            if str(e) == 'list index out of range':
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text=f"К сожалению, в данный момент слишком много желающих отправить донат или приобрести подписку. Попробуйте через несколько минут.")
    elif call.data.split('-')[0] == 'no_asm':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f"Нет так нет! Платёж отменён.")
    elif call.data == 'login_in_bot':
        print("HUY")
        inf = DB.selectDB_users_bot(info=(call.from_user.id,))
        print(inf)
        if not inf:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f"К сожалению, Вы не можете войти в чат" \
                                             f" через подписку бота, ведь у Вас нет подписки! Возможно, вы подписаны через Patreon.")
