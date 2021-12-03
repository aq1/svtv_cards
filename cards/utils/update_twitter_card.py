from typing import Optional

from PIL.Image import Image

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

from .download_image import download_image

generators = {
    'news': generate_news_card,
    'thread': generate_thread_card,
    # 'opinion': generate_opinion_card,
}


@app.task
def update_twitter_card(post: dict) -> dict:
    text: str = post.get('title')
    image_url: str = post.get('feature_image')

    try:
        primary_tag: str = post['primary_tag']['slug']
    except (TypeError, KeyError):
        return {}

    image: Optional[Image] = None

    if not text:
        return {}

    if primary_tag not in generators:
        return {}

    if image_url:
        image = download_image(image_url)

    image = generators[primary_tag](
        text=text,
        image=image,
    )

    response = upload_image(
        image_name=f'{post["id"]}_twitter.jpeg',
        image=image,
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
