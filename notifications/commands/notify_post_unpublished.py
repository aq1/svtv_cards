from ..utils import notify


def notify_post_unpublished(post, _):
    title = post.get('title')
    url = post.get('url')

    message = f'Пост снят с публикации\n{title}\n{url}'
    notify(message=message)
