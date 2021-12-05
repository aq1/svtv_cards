from project.celery import app

from ghost.ghost_admin_request import (
    update_post,
    upload_image,
)

from ..generators import (
    generate_news_card,
    generate_thread_card,
    generate_opinion_card,
)

generators = {
    'news': generate_news_card,
    'thread': generate_thread_card,
    # 'opinion': generate_opinion_card,
}


@app.task
def update_twitter_card(post: dict) -> dict:
    cover = generators[post['primary_tag']['slug']](
        post=post,
    )

    response = upload_image(
        image_name=f'{post["id"]}_twitter.jpeg',
        image=cover,
    )

    if response.status_code != 201:
        return {}

    try:
        image_url = response.json()['images'][0]['url']
    except (KeyError, IndexError):
        return {}

    return update_post(
        post_id=post.get('id'),
        post_updated_at=post.get('updated_at'),
        data={
            'og_image': image_url,
            'twitter_image': image_url,
        },
    ).json()


def update_twitter_card_command(post: dict, previous: dict) -> None:
    fields_to_watch = [
        'title',
        'feature_image',
        'status',
    ]

    if post['twitter_image']:
        if not any([r in previous for r in fields_to_watch]):
            return

    if not post.get('title'):
        return

    try:
        primary_tag: str = post['primary_tag']['slug']
    except (TypeError, KeyError):
        return

    if primary_tag not in generators:
        return

    update_twitter_card.delay(post)
