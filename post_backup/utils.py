from .models import PostBackup


def log_post(post):
    with open('p.txt', 'w') as f:
        f.write(str(post))
    post_backup, _ = PostBackup.objects.get_or_create(ghost_id=post['id'])
    post_backup.post = post
    post_backup.save()
