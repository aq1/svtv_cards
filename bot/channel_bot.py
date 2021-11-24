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


with open('t.txt') as f:
    BOT_TOKEN = f.read().strip()

PATREON_URL = 'https://www.patreon.com/svtvnews'
COMMENTS_URL = 'https://t.me/c/1639121259/{m}?thread={m}'


def callback(update: Update, context: CallbackContext):
    if update.channel_post.reply_markup:
        return

    markup = InlineKeyboardMarkup([[
        InlineKeyboardButton('Patreon', url=PATREON_URL),
        InlineKeyboardButton('Comments', url=COMMENTS_URL.format(m=update.channel_post.message_id))
    ]])
    update.channel_post.edit_reply_markup(markup)


channel_handler = telegram.ext.MessageHandler(
    filters=Filters.update.channel_post & Filters.update.edited_channel_post,
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
