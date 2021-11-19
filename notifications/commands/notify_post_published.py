from ..utils import notify


def notify_post_published(post, _):
    title = post.get('title')
    url = post.get('url')

    try:
        tag = f'#{post["primary_tag"]["name"]}'
    except (TypeError, KeyError):
        tag = ''

    message = f'Новая публикация {tag}\n{title}\n{url}'
    notify.delay(message=message)
