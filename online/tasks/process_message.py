import textwrap

from django.conf import settings
from django.template.loader import render_to_string
from telegram import Bot

from ghost.ghost_admin_request import create_post
from ghost.ghost_admin_request import get_post
from ghost.ghost_admin_request import update_post
from online.models import OnlineMessage
from project.celery import app

PAGE_ID = '6202ca1fbbee620001435e30'


@app.task
def process_message(message_id: str, text: str, html: str):
    online_message, _ = OnlineMessage.objects.get_or_create(
        message_service_id=message_id,
    )

    title = textwrap.shorten(text, width=70, placeholder='...')

    if not online_message.ghost_id:
        post = create_post(title=title)
    else:
        post = get_post(online_message.ghost_id)

    post_html = render_to_string(
        'online/online_message_template.html',
        context={
            'html': html,
            'text': text,
        },
    )

    update_post(
        post_id=post['id'],
        post_updated_at=post['updated_at'],
        data={
            'title': title,
            'html': post_html,
            'tags': [{'name': 'Онлайн'}],
            'authors': ['ruvalerydz@gmail.com'],
        },
    )

    online_message.ghost_id = post['id']
    online_message.message = text
    online_message.save()
    Bot(token=settings.TELEGRAM_TOKEN).send_message(
        settings.TELEGRAM_ADMIN_ID,
        text=f'Saved {online_message}',
    )
