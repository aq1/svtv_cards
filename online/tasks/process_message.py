import textwrap

from django.template.loader import render_to_string

from online.models import OnlineMessage
from project.celery import app

from ghost.ghost_admin_request import get_post
from ghost.ghost_admin_request import create_post
from ghost.ghost_admin_request import update_post


@app.task
def process_message(message_id: str, text: str, html: str):
    online_message, _ = OnlineMessage.objects.get_or_create(
        message_service_id=message_id,
    )

    try:
        title = text.strip().splitlines()[0].split('.')[0]
    except IndexError:
        title = textwrap.shorten(text, width=70, placeholder='...')
    #
    # if online_message.ghost_id:
    #     post = get_post(post_id=online_message.ghost_id)
    # else:
    #     post = create_post(title=title)

    # post_html = render_to_string(
    #     'online/online_message_template.html', {
    #         'html': html,
    #     }
    # )

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

    online_message.text = text
    online_message.ghost_id = post['id']
    online_message.html = html
    online_message.title = title
    online_message.save()
