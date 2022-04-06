from telegram import (
    Bot,
)

from django.conf import settings

from project.celery import app


@app.task
def notify(message):
    Bot(token=settings.TELEGRAM_TOKEN).send_message(
        settings.TELEGRAM_CHAT_ID,
        text=message,
    )
