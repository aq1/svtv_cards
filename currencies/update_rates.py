import os

from django.conf import settings
from telegram import (
    Bot,
    MessageEntity,
)

from project.celery import app


@app.task
def update_rates():
    Bot(token=settings.TELEGRAM_TOKEN).send_message(
        os.getenv('TG'),
        text=f'hi',
    )
