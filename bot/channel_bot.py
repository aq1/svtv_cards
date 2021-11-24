import os

import telegram
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton, Message,
)
from telegram.ext import (
    CallbackContext,
    Filters,
)


BOT_TOKEN = os.environ.get('BOT_TOKEN')

if not BOT_TOKEN:
    with open('t.txt') as f:
        BOT_TOKEN = f.read().strip()

PATREON_URL = 'https://www.patreon.com/svtvnews'
COMMENTS_URL = 'https://t.me/c/1639121259/{m}?thread={m}'


def callback(update: Update, _: CallbackContext):
    message: Message = update.channel_post or update.edited_channel_post
    if message.reply_markup:
        return

    markup = InlineKeyboardMarkup([[
        InlineKeyboardButton('Patreon', url=PATREON_URL),
        InlineKeyboardButton('Comments', url=COMMENTS_URL.format(m=message.message_id))
    ]])
    message.edit_reply_markup(markup)


channel_handler = telegram.ext.MessageHandler(
    filters=Filters.update.channel_post | Filters.update.edited_channel_post,
    callback=callback,
)

if __name__ == '__main__':
    _bot = telegram.Bot(token=BOT_TOKEN)
    updater = telegram.ext.Updater(bot=_bot, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(channel_handler)
    updater.start_polling(
        drop_pending_updates=True,
        timeout=5,
        poll_interval=0.5,
    )
