import json

from django.template.loader import render_to_string

from ghost.ghost_admin_request import create_post, get_post, update_post
from project.celery import app
from ..models import OnlineAttachment
from ..models import OnlineMessage


@app.task
def upload_online_message_to_ghost(message_id):
    message = OnlineMessage.objects.filter(id=message_id).first()

    if not message:
        return

    attachments = OnlineAttachment.objects.filter(message_id=message_id)
    for each in attachments:
        each.meta = json.loads(each.meta.replace("'", '"'))

    attachment_rows = []
    for i in range(0, len(attachments), 3):
        attachment_rows.append(attachments[i:i + 3])

    html = render_to_string(
        'online/online_message_template.html', {
            'message': message,
            'attachments': attachment_rows,
        },
    )

    if message.ghost_id:
        post = get_post(post_id=message.ghost_id)
    else:
        post = create_post(title=message.title)

    r = update_post(
        post_id=post['id'],
        post_updated_at=post['updated_at'],
        data={
            'title': message.title,
            'html': html,
            'status': 'published',
            'tags': [{'name': 'Онлайн'}],
            'authors': ['ruvalerydz@gmail.com'],
        },
    )

    r.raise_for_status()

    message.ghost_id = post['id']
    message.save()
