from collections import defaultdict

from django.template.loader import render_to_string
from django.utils import timezone

from ghost.ghost_admin_request import get_page
from ghost.ghost_admin_request import update_page
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
