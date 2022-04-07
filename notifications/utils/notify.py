from telegram import (
    Bot,
    MessageEntity,
)

from django.conf import settings

from project.celery import app


@app.task
def notify(message, username=''):
    entities = []
    if username:
        message = f'{username} {message}'
        entities = [MessageEntity('mention', 0, len(username))]

    Bot(token=settings.TELEGRAM_TOKEN).send_message(
        settings.TELEGRAM_CHAT_ID,
        text=message,
        entities=entities,
    )
