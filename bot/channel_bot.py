import os

import telegram
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    CallbackContext,
    Filters,
)

BOT_TOKEN = os.environ.get('BOT_TOKEN')

CHANNEL_ID = -1001513669961
PATREON_URL = 'https://www.patreon.com/svtvnews'

if not BOT_TOKEN:
    with open('t.txt') as f:
        BOT_TOKEN = f.read().strip()


def callback(update: Update, context: CallbackContext):
    try:
        channel_id = update.message.forward_from_chat.id
    except AttributeError:
        return

    if channel_id != CHANNEL_ID:
        return

    if update.message.reply_markup:
        return

    markup = InlineKeyboardMarkup([[
        InlineKeyboardButton('Patreon', url=PATREON_URL),
        InlineKeyboardButton('Comments', url=f'{update.message.link}?thread={update.message.message_id}')
    ]])

    context.bot.edit_message_reply_markup(
        chat_id=CHANNEL_ID,
        message_id=update.message.forward_from_message_id,
        reply_markup=markup,
    )


channel_handler = telegram.ext.MessageHandler(
    filters=Filters.update.message,
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
