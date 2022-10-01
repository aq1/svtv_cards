import pytz
import json
from aiogram import types, executor
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, BotCommand, BotCommandScopeAllGroupChats
from ast import literal_eval as leval
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegraph import Telegraph
from config import bot, chat_id, db as DB, dp, actual_pattern
from mini_logs import log
from tgstat_helper import check_status
from planner import spin_pattern
from states import State_SVTV

telegraph = Telegraph('cba32cb794981b63f6e4da5d19783c4176f6fb0813a879a5d3ab3c1f9197')

def auth(func):
    async def wrapper(message):
        if message.chat.id != chat_id:
            return
        return await func(message)
    return wrapper

def patterns(id_patterns_start, id_patterns_end):
    patterns_menu = InlineKeyboardMarkup()
    selected = DB.select_several_patternDB(info=(id_patterns_start, id_patterns_end,))
    if selected == []:
        id_patterns_start = id_patterns_start-10
        id_patterns_end = id_patterns_end-10
    next = InlineKeyboardButton('>', callback_data=f"next_pattern-{id_patterns_end}")
    number = InlineKeyboardButton(f"{str(id_patterns_end)[:-1]}", callback_data="stopnum")
    back = InlineKeyboardButton('<', callback_data=f"back_pattern-{id_patterns_end}")
    for x in selected:
        name_pattern = InlineKeyboardButton(f"{x[1]}", callback_data=f"pattern-{x[0]}")
        patterns_menu.add(name_pattern)
        print(x)
    patterns_menu.add(back, number, next)
    return patterns_menu

def words(id_pattern, id_words_start, id_words_end, start, number_menu):
    if (number_menu) == 0 or number_menu == 6:
        return words
    try:
        if int(start) == 0:
            words_menu = InlineKeyboardMarkup(row_width=2)
            selected = DB.select_several_wordDB2(info=(id_pattern,))
            id_words_start = selected[0][0]
            id_words_end = id_words_start + 9
            selected_number = DB.select_several_wordDB(info=(id_words_start, id_words_end))
            change_name = InlineKeyboardButton(f'🔻 Изменить название паттерна 🔻',
            callback_data=f"change_name-{id_pattern}")
            next = InlineKeyboardButton('>', callback_data=f"next_word-{id_words_end}-{id_pattern}-{number_menu}")
            number = InlineKeyboardButton(f"{number_menu}", callback_data="stopnum")
            back = InlineKeyboardButton('<', callback_data=f"back_word-{id_words_end}-{id_pattern}-{number_menu}")
            back_menu = InlineKeyboardButton('в меню', callback_data=f"back_menu_words")
            opt = InlineKeyboardButton('✅ Выбрать паттерн', callback_data=f"opt-{id_pattern}")
            t = []
            for x in selected_number:
                button_text = x[1]
                if x[2]:
                    button_text = f'🔹{x[2]}'
                name_word = InlineKeyboardButton(
                    button_text,
                    callback_data=f"word-{id_pattern}-{x[0]}-{id_words_start}-{id_words_end}-{start}-{number_menu}",
                )
                t.append(name_word)
            words_menu.add(change_name)
            words_menu.add(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9])
            words_menu.row(back, number, next).row(opt).row(back_menu)
            return words_menu
        elif int(start) == 1:
            words_menu = InlineKeyboardMarkup(row_width=2)
            selected = DB.select_several_wordDB2(info=(id_pattern,))
            selected_number = DB.select_several_wordDB(info=(id_words_start, id_words_end))
            if selected_number[0][3] != int(id_pattern):
                return words
            change_name = InlineKeyboardButton(f'🔻 Изменить название паттерна 🔻',
            callback_data=f"change_name-{id_pattern}")
            next = InlineKeyboardButton('>', callback_data=f"next_word-{id_words_end}-{id_pattern}-{number_menu}")
            number = InlineKeyboardButton(f"{number_menu}", callback_data="stopnum")
            back = InlineKeyboardButton('<', callback_data=f"back_word-{id_words_end}-{id_pattern}-{number_menu}")
            back_menu = InlineKeyboardButton('в меню', callback_data=f"back_menu_words")
            opt = InlineKeyboardButton('✅ Выбрать паттерн', callback_data=f"opt-{id_pattern}")
            t = []
            for x in selected_number:
                name_word = x[1]
                name_word = InlineKeyboardButton(f"{x[1]}",
                callback_data=f"word-{id_pattern}-{x[0]}-{id_words_start}-{id_words_end}-{start}-{number_menu}")
                t.append(name_word)
            words_menu.add(change_name)
            words_menu.add(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9])
            words_menu.row(back, number, next).row(opt).row(back_menu)
            return words_menu
    except Exception as e:
        print(e)

def word(id_pattern, id_word, id_words_start, id_words_end, start, number_menu):
    word_menu = InlineKeyboardMarkup()
    change_name_word = InlineKeyboardButton(f'🔻 Изменить название слова 🔻',
    callback_data=f"change_name_word-{id_pattern}-{id_word}-{id_words_start}-{id_words_end}-{start}-{number_menu}")
    off_word = InlineKeyboardButton(f'Удалить слово', callback_data=f"off_word-{id_word}")
    change_name_minusword = InlineKeyboardButton(f'🔹 Изменить название минус-слова 🔹',
    callback_data=f"change_name_minusword-{id_pattern}-{id_word}-{id_words_start}-{id_words_end}-{start}-{number_menu}")
    off_minusword = InlineKeyboardButton(f'Удалить минус-слово', callback_data=f"off_minusword-{id_word}")
    back = InlineKeyboardButton('назад',
    callback_data=f"back_word_menu-{id_pattern}-{id_words_start}-{id_words_end}-{start}-{number_menu}")
    back_menu = InlineKeyboardButton('в меню', callback_data=f"back_menu_words")
    word_menu.add(change_name_word).row(off_word).row(change_name_minusword).row(off_minusword).row(back).row(back_menu)
    return word_menu

@dp.callback_query_handler(lambda c: True, state='*')
async def inline_handler(call: types.CallbackQuery, state: FSMContext):
    try:
        print(call.data.split('-'))
        if call.data.split('-')[0] == "pattern":
            id_pattern = call.data.split('-')[1]
            name_pattern = DB.select_patternDB(info=(id_pattern,))[1]
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=f'Паттерн {name_pattern}', reply_markup=words(id_pattern, 0, 0, 0, 1))
        elif call.data.split('-')[0] == "back_menu_words":
            data = DB.select_actual_patternDB()
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=f'Текущий паттерн — <strong>{data[1]}</strong>.', reply_markup=patterns(0, 10,))
        elif call.data.split('-')[0] == "next_pattern":
            id_patterns_start = call.data.split('-')[1]
            id_patterns_end = int(id_patterns_start) + 10
            data = DB.select_actual_patternDB()
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=f'Текущий паттерн — <strong>{data[1]}</strong>.', reply_markup=patterns(id_patterns_start, id_patterns_end))
        elif call.data.split('-')[0] == "back_pattern":
            id_patterns_start = int(call.data.split('-')[1]) - 10
            if id_patterns_start <= 0:
                return
            id_patterns_end = int(id_patterns_start) - 10
            data = DB.select_actual_patternDB()
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=f'Текущий паттерн — <strong>{data[1]}</strong>.', reply_markup=patterns(id_patterns_end, id_patterns_start))
        if call.data.split('-')[0] == "word":
            id_pattern = call.data.split('-')[1]
            id_word = call.data.split('-')[2]
            id_words_start = call.data.split('-')[3]
            id_words_end = call.data.split('-')[4]
            start = call.data.split('-')[5]
            name_word = DB.select_wordDB(info=(id_word,))[0]
            number_menu = int(call.data.split('-')[6])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=f'Слово {name_word}', reply_markup=word(id_pattern, id_word, id_words_start, id_words_end, start, number_menu))
        elif call.data.split('-')[0] == "next_word":
            id_word_start = int(call.data.split('-')[1]) + 1
            id_pattern = call.data.split('-')[2]
            number_menu = int(call.data.split('-')[3])
            id_word_end = int(id_word_start) + 9
            number_menu = number_menu + 1
            data = DB.select_actual_patternDB()
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=f'Паттерн <strong>{data[1]}</strong>', 
            reply_markup=words(id_pattern, id_word_start, id_word_end, 1, number_menu), parse_mode="HTML")
        elif call.data.split('-')[0] == "back_word":
            id_word_start = int(call.data.split('-')[1]) - 10
            id_pattern = call.data.split('-')[2]
            number_menu = int(call.data.split('-')[3])
            id_word_end = int(id_word_start) - 9
            number_menu = number_menu - 1
            data = DB.select_actual_patternDB()
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=f'Паттерн <strong>{data[1]}</strong>',
            reply_markup=words(id_pattern, id_word_end, id_word_start, 1, number_menu), parse_mode="HTML")
        elif call.data.split('-')[0] == "back_word_menu":
            id_pattern = int(call.data.split('-')[1])
            id_words_start = int(call.data.split('-')[2])
            id_words_end = int(call.data.split('-')[3])
            start = int(call.data.split('-')[4])
            name_pattern = DB.select_patternDB(info=(id_pattern,))[1]
            number_menu = int(call.data.split('-')[5])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=f'Паттерн {name_pattern}', reply_markup=words(id_pattern, id_words_start, id_words_end, start, number_menu))
        elif call.data.split('-')[0] == "opt":
            id_pattern = int(call.data.split('-')[1])
            name_pattern = DB.select_patternDB(info=(id_pattern,))[1]
            DB.update_actual_patternDB(id_pattern=id_pattern, name_pattern=name_pattern)
            actual_pattern.update({"actual_word_id": -1})
            await bot.send_message(chat_id=call.message.chat.id, text=f'Актуальный паттерн успешно сменён на ' \
            f'<strong>{name_pattern}</strong>')
        elif call.data.split('-')[0] == "change_name":
            id_pattern = int(call.data.split('-')[1])
            name_pattern = DB.select_patternDB(info=(id_pattern,))[1]
            await bot.send_message(chat_id=call.message.chat.id, text=f'Введите новое название паттерна для <strong>' \
            f'{name_pattern}</strong>.')
            await state.update_data(id_pattern=id_pattern, name_pattern_old=name_pattern)
            await State_SVTV.name_pattern.set()
        elif call.data.split('-')[0] == "change_name_word":
            id_pattern = int(call.data.split('-')[1])
            id_word = int(call.data.split('-')[2])
            id_words_start = int(call.data.split('-')[3])
            id_words_end = int(call.data.split('-')[4])
            start = int(call.data.split('-')[5])
            name_pattern = DB.select_patternDB(info=(id_pattern,))[1]
            name_word = DB.select_wordDB(info=(id_word,))[0]
            number_menu = int(call.data.split('-')[6])
            await bot.send_message(chat_id=call.message.chat.id, text=f'Введите новое слово заместо <strong>{name_word}</strong>.')
            await state.update_data(id_pattern=id_pattern, id_word=id_word, id_words_start=id_words_start, id_words_end=id_words_end,
            start=start, name_pattern=name_pattern, name_word=name_word, number_menu=number_menu)
            await State_SVTV.name_word.set()
        elif call.data.split('-')[0] == "change_name_minusword":
            id_pattern = int(call.data.split('-')[1])
            id_word = int(call.data.split('-')[2])
            id_words_start = int(call.data.split('-')[3])
            id_words_end = int(call.data.split('-')[4])
            start = int(call.data.split('-')[5])
            name_pattern = DB.select_patternDB(info=(id_pattern,))[1]
            name_word = DB.select_wordDB(info=(id_word,))[1]
            number_menu = int(call.data.split('-')[6])
            await bot.send_message(chat_id=call.message.chat.id, text=f'Введите новое минус-слово заместо <strong>{name_word}</strong>.')
            await state.update_data(id_pattern=id_pattern, id_minusword=id_word, id_words_start=id_words_start, id_words_end=id_words_end,
            start=start, name_pattern=name_pattern, name_word=name_word, number_menu=number_menu)
            await State_SVTV.name_minusword.set()
        elif call.data.split('-')[0] == "off_word":
            id_word = call.data.split('-')[1]
            name_word = DB.select_wordDB(info=(id_word,))[0]
            DB.update_wordDB(info=(" ", id_word))
            actual_pattern.update({"actual_word_id": -1})
            await bot.send_message(chat_id=call.message.chat.id, text=f'Слово <strong>{name_word}</strong> удалено.')
        elif call.data.split('-')[0] == "off_minusword":
            id_word = call.data.split('-')[1]
            name_minusword = DB.select_wordDB(info=(id_word,))[1]
            DB.update_minus_wordDB(info=(" ", id_word))
            await bot.send_message(chat_id=call.message.chat.id, text=f'Минус-слово <strong>{name_minusword}</strong> удалено.')
        await call.answer()
    except Exception as e:
        log(str(e), "inline_handler")

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply(f'Тут старт\nID: {message.chat.id}')

@dp.message_handler(commands=['cancel'])
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Отменено")

@dp.message_handler(commands=['setting'])
@auth
async def setting(message: types.Message):
    data = DB.select_actual_patternDB()
    await message.reply(f'Текущий паттерн — <strong>{data[1]}</strong>.', reply_markup=patterns(0, 10,), parse_mode="HTML")

@dp.message_handler(commands=['status'])
@auth
async def status(message: types.Message):
    await message.reply(check_status())

@dp.message_handler(commands=['ban'])
@auth
async def blacklist_add(message: types.Message):
    try:
        id = message['reply_to_message']['forward_from_chat']['id']
        name_channel = message['reply_to_message']['forward_from_chat']['title'][:50]
        data = leval(DB.select_channelDB()) if DB.select_channelDB() else []
        if id in data:
            await message.reply('Данный канал уже занесён в Чёрный список.')
            return
        data.append(id)
        DB.update_channelDB(info=(str(data),))
        with open('blacklist.json', 'r') as f:
            args = json.load(f)
        args.update({id: name_channel})
        with open('blacklist.json', 'w') as f:
            json.dump(args, f, indent=4)
        await message.reply(f'{name_channel} | {id} успешно занесён в Чёрный список!')
    except Exception as e:
        if str(type(e)) == "<class 'KeyError'>": 
            await message.reply(f"Извините, но похоже, что данный канал уже занесён в Чёрный список!")
        log(str(e), "blacklist_add")

@dp.message_handler(commands=['unban'])
@auth
async def blacklist_remove(message: types.Message):
    try:
        id = message['reply_to_message']['forward_from_chat']['id']
        name_channel = message['reply_to_message']['forward_from_chat']['title']
        data = leval(DB.select_channelDB()) if DB.select_channelDB() else []
        if id not in data:
            await message.reply('Данного канала нет в Чёрном списке.')
            return
        data.remove(id)
        DB.update_channelDB(info=(str(data),))
        with open('blacklist.json', 'r') as f:
            args = json.load(f)
        args.pop(str(id))
        with open('blacklist.json', 'w') as f:
            json.dump(args, f, indent=4)
        await message.reply(f'{name_channel} | {id} успешно вынесен из Чёрного списка!')
    except Exception as e:
        if str(type(e)) == "<class 'KeyError'>": 
            await message.reply(f"Извините, но похоже, что данного канала нет в Чёрном списке!")
        log(str(e), "blacklist_remove")

@dp.message_handler(commands=['bl'])
@auth
async def blacklist(message: types.Message):
    try:
        with open('blacklist.json', 'r') as f:
            args = json.load(f)
        if not args:
            return await message.reply("Чёрный список пуст")
        channels = ['Чёрный список каналов: <br>']
        i, index = 0, 0
        for x in args:
            i += 1
            if i > 420:
                channels.append("Чёрный список каналов: <br>")
                index += 1
                i = 0
            channels[index] += f'<ol>{x} | {args[x]}</ol>'
        answer = 'Чёрный список:'
        for x in channels:
            r = telegraph.create_page(
                "".join(f"Black list"),
                html_content=f"{x}", author_name='murix'
            )
            answer += f"\n - {r['url']}"
        await message.reply(answer)
    except Exception as e:
        if str(e) == "CONTENT_TOO_BIG":
            print('Ошибка')
        log(str(e), "blacklist")

@dp.message_handler(state=State_SVTV.name_pattern)
async def svtv_state_name_pattern(message: types.Message, state: FSMContext):
    try:
        name_pattern = message.text
        info_pattern = await state.get_data()
        id_pattern = info_pattern["id_pattern"]
        name_pattern_old = info_pattern["name_pattern_old"]
        DB.update_patternDB(info=(name_pattern, id_pattern))
        await message.reply(f'Вы успешно сменили название паттерна <strong>{name_pattern_old}</strong> на <strong>{name_pattern}</strong>',
        parse_mode="HTML")
        await state.finish()
    except Exception as e:
        log(str(e), "svtv_state_name_pattern")

@dp.message_handler(state=State_SVTV.name_word)
async def svtv_state_name_word(message: types.Message, state: FSMContext):
    try:
        name_word = message.text
        info_word = await state.get_data()
        id_pattern = info_word["id_pattern"]
        id_word = info_word["id_word"]
        id_words_start = info_word["id_words_start"]
        id_words_end = info_word["id_words_end"]
        start = info_word["start"]
        name_old_word = info_word["name_word"]
        number_menu = info_word["number_menu"]
        DB.update_wordDB(info=(name_word, id_word))
        await message.reply(f'Вы успешно сменили название слова <strong>{name_old_word}</strong> на <strong>{name_word}</strong>',
        parse_mode="HTML", reply_markup=word(id_pattern, id_word, id_words_start, id_words_end, start, number_menu))
        await state.finish()
    except Exception as e:
        log(str(e), "svtv_state_name_word")

@dp.message_handler(state=State_SVTV.name_minusword)
async def svtv_state_name_minusword(message: types.Message, state: FSMContext):
    try:
        name_word = message.text
        info_word = await state.get_data()
        id_pattern = info_word["id_pattern"]
        id_minusword = info_word["id_minusword"]
        id_words_start = info_word["id_words_start"]
        id_words_end = info_word["id_words_end"]
        start = info_word["start"]
        name_old_word = info_word["name_word"]
        number_menu = info_word["number_menu"]
        DB.update_minus_wordDB(info=(name_word, id_minusword))
        await message.reply(f'Вы успешно сменили название минус-слова <strong>{name_old_word}</strong> на <strong>{name_word}</strong>'\
        f'\n\nСлово <strong>{DB.select_wordDB(info=(id_minusword,))[0]}</strong>',
        parse_mode="HTML", reply_markup=word(id_pattern, id_minusword, id_words_start, id_words_end, start, number_menu))
        await state.finish()
    except Exception as e:
        log(str(e), "svtv_state_name_word")

async def set_commands():
    await dp.bot.set_my_commands(commands=[
        BotCommand('setting', 'Настройки'),
        BotCommand('ban', 'Внести канал в ЧС'),
        BotCommand('unban', 'Вынести канал из ЧС'),
        BotCommand('bl', 'Просмотреть ЧС'),
        BotCommand('status', 'Статус API')
    ], scope=BotCommandScopeAllGroupChats())

async def on_startup(dp):
    try:
        scheduler = AsyncIOScheduler(timezone=pytz.timezone('Europe/Moscow'))
        # scheduler.add_job(spin_pattern, "cron", second="*/15")
        scheduler.add_job(spin_pattern, "cron", minute="*/4")
        scheduler.start()
        await set_commands()
    except Exception as e:
        log(str(e), 'on_startup')

if __name__ == '__main__':
    DB.setupDB()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)