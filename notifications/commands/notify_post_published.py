from ..utils import notify


def notify_post_published(post, _):
    title = post.get('title')
    url = post.get('url')
    tag = post.get('primary_tag', {}).get('name')

    message = f'Опубликован пост с тэгом "{tag}"\n{title}\n{url}'
    notify.delay(message=message)
