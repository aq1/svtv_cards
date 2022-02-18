import textwrap

from django.conf import settings
from telegram import Bot

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
        title = textwrap.shorten(text, width=70, placeholder='...')

    online_message.text = text
    online_message.html = html
    online_message.title = title
    online_message.save()

    Bot(token=settings.CHANNEL_BOT_TOKEN).send_message(
        settings.TELEGRAM_ADMIN_ID,
        text=f'Saved {online_message}',
    )

    update_online_page.delay()
