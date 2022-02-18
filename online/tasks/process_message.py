import textwrap

from django.conf import settings
from telegram import Bot

from ghost.ghost_admin_request import create_post
from ghost.ghost_admin_request import get_post
from ghost.ghost_admin_request import update_post
from online.models import OnlineMessage
from project.celery import app

from .update_online_page import update_online_page


@app.task
def process_message(message_id: str, text: str, html: str):
    online_message, _ = OnlineMessage.objects.get_or_create(
        message_service_id=message_id,
    )

    try:
        title = text.strip().splitlines()[0].split('.')[0]
    except IndexError:
        title = text

    title = textwrap.shorten(title, width=70, placeholder='...')

    if not online_message.ghost_id:
        post = create_post(title=title)
    else:
        post = get_post(online_message.ghost_id)

    update_post(
        post_id=post['id'],
        post_updated_at=post['updated_at'],
        data={
            'title': title,
            'tags': [{'name': '#Онлайн'}],
            'authors': ['ruvalerydz@gmail.com'],
            'status': 'published',
        },
    )

    online_message.ghost_id = post['id']
    online_message.text = text
    online_message.html = html
    online_message.save()
    Bot(token=settings.CHANNEL_BOT_TOKEN).send_message(
        settings.TELEGRAM_ADMIN_ID,
        text=f'Saved {online_message}',
    )

    update_online_page.delay()
