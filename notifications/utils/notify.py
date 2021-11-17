from telegram import (
    Bot,
    MessageEntity,
)

from django.conf import settings

from project.celery import app


@app.task
def notify(message):
    Bot(token=settings.TELEGRAM_TOKEN).send_message(
        settings.TELEGRAM_CHAT_ID,
        text=f'{settings.TELEGRAM_USER} {message}',
        entities=[MessageEntity('mention', 0, len(settings.TELEGRAM_USER))],
    )
