import textwrap
from collections import defaultdict

from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from telegram import Bot

from ghost.ghost_admin_request import create_post
from ghost.ghost_admin_request import get_page
from ghost.ghost_admin_request import get_post
from ghost.ghost_admin_request import update_page
from ghost.ghost_admin_request import update_post
from online.models import OnlineMessage
from project.celery import app


@app.task
def update_online_page():
    messages = OnlineMessage.objects.filter(

    ).order_by(
        '-created_at',
    )[:50]

    sorted_messages = defaultdict(list)
    for message in messages:
        sorted_messages[message.created_at.date()].append(message)

    sorted_messages = [[k, sorted_messages[k]] for k in reversed(sorted(sorted_messages.keys()))]
    today = timezone.now().date()
    yesterday = today - timezone.timedelta(days=1)

    html = render_to_string(
        'online/online_message_template.html',
        context={
            'online_messages': sorted_messages,
            'today': today,
            'yesterday': yesterday,
        },
    )

    page = get_page(page_slug='online')
    update_page(
        page_id=page['id'],
        page_updated_at=page['updated_at'],
        data={
            'html': html,
            'authors': ['ruvalerydz@gmail.com'],
        },
    )


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
