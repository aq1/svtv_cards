from ..utils import notify

PREFERABLE_URL_LENGTH = 200


def verify_post(post: dict) -> list[str]:
    url = post.get('url', '')
    slug = post.get('slug', '')
    title = post.get('title', '')

    warnings = []

    if 'untitled' in slug:
        warnings.append(f'❗️ Untitled в URL')

    if '  ' in title:
        warnings.append(f'⚠️ Двойной пробел в названии')

    if len(url) > PREFERABLE_URL_LENGTH:
        warnings.append(f'⚠️ Ссылка длиннее {PREFERABLE_URL_LENGTH} символов')

    return warnings


def notify_post_published(post, _):
    title = post.get('title')
    url = post.get('url')

    try:
        tag = f'#{post["primary_tag"]["name"]}'
    except (TypeError, KeyError):
        return

    message = f'Новая публикация {tag}\n{title}\n{url}'
    warnings = '\n'.join(verify_post(post))

    if warnings:
        message = f'{message}\n{warnings}'

    notify.apply_async(kwargs={'message': message}, countdown=10)
