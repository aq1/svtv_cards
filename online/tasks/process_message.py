import textwrap

import telegram
from django.conf import settings
from django.db import models

from online.models import OnlineMessage, OnlineAttachment
from project.celery import app
from .upload_file import upload_file


@app.task
def process_message(message_id: str, text: str, html: str, media_group_id: str, attachment):
    online_message = OnlineMessage.objects.filter(
        models.Q(message_service_id=message_id) | models.Q(media_group_id=media_group_id),
    ).first()

    if not online_message:
        online_message = OnlineMessage(
            message_service_id=message_id,
            media_group_id=media_group_id or '',
        )

    try:
        title = text.strip().splitlines()[0].split('.')[0]
    except IndexError:
        title = textwrap.shorten(text, width=70, placeholder='...')

    # if online_message.ghost_id:
    #     post = get_post(post_id=online_message.ghost_id)
    # else:
    #     post = create_post(title=title)
    #
    # post_html = render_to_string(
    #     'online/online_message_template.html', {
    #         'html': html,
    #     }
    # )
    #
    # update_post(
    #     post_id=post['id'],
    #     post_updated_at=post['updated_at'],
    #     data={
    #         'title': title,
    #         'html': post_html,
    #         'status': 'published',
    #         'tags': [{'name': '#Онлайн'}],
    #         'authors': ['ruvalerydz@gmail.com'],
    #     },
    # )

    # online_message.ghost_id = 'post['id']'
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

        online_attachment.meta = attachment
        online_attachment.url = url
        online_attachment.save()
