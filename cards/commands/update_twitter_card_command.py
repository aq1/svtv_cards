from typing import Optional

from project.celery import app

from ghost.ghost_admin_request import (
    update_post,
    upload_image,
)

from ..generators import (
    generate_news_card,
    generate_thread_card,
    generate_opinion_card,
    generate_factchecking_card,
)
from ..utils.factchecking import (
    get_factchecking_meter_tag,
    get_factchecking_tag_label,
)

generators = {
    'news': generate_news_card,
    'thread': generate_thread_card,
    'opinion': generate_opinion_card,
    'factchecking': generate_factchecking_card,
}


def create_post_cover(post: dict) -> Optional[str]:
    cover = generators[post['primary_tag']['slug']](
        post=post,
    )

    response = upload_image(
        image_name=f'{post["id"]}_twitter.jpeg',
        image=cover,
    )

    if response.status_code != 201:
        return

    try:
        return response.json()['images'][0]['url']
    except (KeyError, IndexError):
        return


def get_factchecking_meta_fields(post: dict) -> dict[str, str]:
    tag: str = get_factchecking_meter_tag(post)
    meta_title: str = f'{post["feature_image_caption"]}: {get_factchecking_tag_label(tag)}'
    meta_description: str = 'Мы все проверили, и вот наш вердикт'

    return {
        'og_title': meta_title,
        'twitter_title': meta_title,
        'meta_title': meta_title,
        'og_description': meta_description,
        'twitter_description': meta_description,
        'meta_description': meta_description,
    }


@app.task
def update_post_fields(post: dict) -> dict:
    cover_url = create_post_cover(post)

    if not cover_url:
        return {}

    data = {
        'og_image': cover_url,
        'twitter_image': cover_url,
    }

    if post['primary_tag']['slug'] == 'factchecking':
        data.update(get_factchecking_meta_fields(post))

    return update_post(
        post_id=post.get('id'),
        post_updated_at=post.get('updated_at'),
        data=data,
    ).json()


def update_post_fields_command(post: dict, previous: dict) -> None:
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

    update_post_fields.delay(post)
