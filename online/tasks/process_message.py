import textwrap

import telegram
from django.conf import settings
from django.db import models

from project.celery import app
from online.models import OnlineMessage, OnlineAttachment
from online.tasks.upload_file import upload_file
from online.tasks.upload_online_message_to_ghost import upload_online_message_to_ghost


@app.task
def process_message(message_id: str, chat_id: str, text: str, html: str, media_group_id: str, attachment):
    online_message = OnlineMessage.objects.filter(
        models.Q(message_service_id=message_id) | models.Q(media_group_id=media_group_id),
    ).first()

    if not online_message:
        online_message = OnlineMessage(
            message_service_id=message_id,
            chat_id=chat_id,
            media_group_id=media_group_id or '',
        )

    try:
        title = text.strip().splitlines()[0].split('.')[0]
    except IndexError:
        title = textwrap.shorten(text, width=70, placeholder='...')

    if text:
        online_message.text = text

    if html:
        online_message.html = html

    if title:
        online_message.title = title

    online_message.save()

    if attachment:
        online_attachment, created = OnlineAttachment.objects.get_or_create(
            message=online_message,
            attachment_id=attachment['file_unique_id'],
        )

        if not created:
            return

        bot = telegram.Bot(token=settings.CHANNEL_BOT_TOKEN)
        filename = bot.get_file(attachment['file_id']).download()
        url = upload_file(filename)

        if attachment.get('thumb'):
            filename = bot.get_file(attachment['thumb']['file_id']).download()
            attachment['thumb']['url'] = upload_file(filename)

        online_attachment.meta = attachment
        online_attachment.url = url
        online_attachment.save()

    upload_online_message_to_ghost.apply_async(
        kwargs={'message_id': online_message.id},
        countdown=60,
    )
