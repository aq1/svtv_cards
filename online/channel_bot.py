from itertools import chain
from urllib.parse import urlparse, urlunparse

import telegram
from django.conf import settings
from telegram import (
    Update,
    Message,
)
from telegram.ext import (
    CallbackContext,
    Filters,
)

from online.tasks import process_message


def handle_channel_message(update: Update, _: CallbackContext):
    post: Message = update.channel_post or update.edited_channel_post
    text = post.text or post.caption or ''

    for entity in chain(post.entities, post.caption_entities):
        if entity.type in ('url', 'text_link'):
            url = getattr(entity, 'url') or text[entity.offset:entity.offset + entity.length]
            parsed_url = urlparse(url)
            if not parsed_url.scheme:
                url = f'https://{urlunparse(parsed_url)}'

            if urlparse(url).hostname == 'svtv.org':
                return

    attachment = post.effective_attachment
    if isinstance(attachment, list):
        attachment = attachment[-2]

    process_message.delay(
        message_id=post.message_id,
        text=text,
        html=post.text_html_urled or post.caption_html_urled or '',
        media_group_id=post.media_group_id,
        attachment=attachment.to_dict(),
    )


channel_handler = telegram.ext.MessageHandler(
    filters=Filters.update.channel_posts,
    callback=handle_channel_message,
)


def start():
    _bot = telegram.Bot(token=settings.CHANNEL_BOT_TOKEN)
    print(f'{_bot.first_name} started')
    updater = telegram.ext.Updater(bot=_bot, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(channel_handler)
    updater.start_polling(
        drop_pending_updates=True,
        timeout=5,
        poll_interval=0.5,
    )
