from asyncio import get_event_loop

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from DBworker import DB

# это всё необходимо заполнить
token = ''  # токен бота
chat_id = -1  # айди чата
admins = [
    1,
]  # админы бота, которые смогут использовать whitelist и функцию проверки на действительность подписок в любое время
cents = 2000  # сумма подписки для доступа в чат
address = '0.0.0.0:8000'  # Адрес, где будет запущен веб-сервер для патреона
redirect_uri = 'http://localhost:8000/'  # Урл перенаправления, который указан в клиенте на аккаунте на патреоне
client_id = ''  # Айди клиента
client_secret = ''  # Секрет клиента

bot = Bot(token=token, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage(), loop=get_event_loop())
db = DB()
