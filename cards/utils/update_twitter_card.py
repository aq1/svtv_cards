from typing import Optional

from PIL import Image

from project.celery import app
from ..generators import (
    generate_news_card,
    generate_thread_card,
    generate_opinion_card,
)
from ghost.ghost_admin_request import (
    update_post,
    upload_image,
)


generators = {
    'news': generate_news_card,
    'thread': generate_thread_card,
    'opinion': generate_opinion_card,
}


@app.task
def update_twitter_card(post: dict) -> dict:
    text: str = post.get('title')

    try:
        primary_tag: str = post['primary_tag']['slug']
    except (TypeError, KeyError):
        return {}

    if not text:
        return {}

    if primary_tag not in generators:
        return {}

    cover: Optional[Image.Image] = None

    cover = generators[primary_tag](
        post=post,
        cover=cover,
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
        }
    ).json()
