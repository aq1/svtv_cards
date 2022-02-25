from .models import PostBackup

from project.celery import app


@app.task
def log_post(post):
    post_backup, _ = PostBackup.objects.get_or_create(ghost_id=post['id'])
    post_backup.post = post
    post_backup.title = post['title']
    post_backup.save()
