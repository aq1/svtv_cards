from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from DBworker import DB

# это всё необходимо заполнить
token = ''  # токен бота
chat_id = ''  # айди чата
tgstat_token = ''  # токен для api.tgstat.ru

bot = Bot(token, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())
db = DB()
