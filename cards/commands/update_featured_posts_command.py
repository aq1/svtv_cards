from project.celery import app
from ghost.ghost_api_request import browse_posts
from ghost.ghost_admin_request import update_post

TAGS_ALLOWED_TO_BE_FEATURED = {
    'news',
    'thread',
    'opinion',
    'factchecking',
    'test',
}


def unfeature_post(post: dict):
    update_post(
        post_id=post['id'],
        post_updated_at=post['updated_at'],
        data={
            'featured': False,
        },
    )


@app.task
def update_featured_posts() -> None:
    # обязательно чтобы были заферены
    # по одному мнению и переводу
    # и два любых других поста

    # как-то запутанно получилось

    counter = {
        'translation': 0,
        'opinion': 0,
        'others': 0,
    }

    posts = browse_posts(
        request_filter='featured:true',
        include=['tags'],
    )

    for post in posts:
        if post['primary_tag']['slug'] not in ('translation', 'opinion'):
            counter['others'] += 1
            if counter['others'] > 2:
                unfeature_post(post)
        else:
            counter[post['primary_tag']['slug']] += 1
            if counter[post['primary_tag']['slug']] > 1:
                unfeature_post(post)


def update_featured_posts_command(post: dict, _: dict) -> None:
    if not post.get('title'):
        return

    if not post.get('featured'):
        return

    try:
        primary_tag: str = post['primary_tag']['slug']
    except (TypeError, KeyError):
        return

    if primary_tag not in TAGS_ALLOWED_TO_BE_FEATURED:
        return

    update_featured_posts()
