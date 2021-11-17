import io
from typing import Optional

import requests
from PIL import (
    Image,
)
from PIL.Image import Image as ImageType

from project.celery import app
from .generate_twitter_news_card import generate_twitter_news_card
from ghost.ghost_admin_request import (
    update_post,
    upload_image,
)


def download_image(image_url: str) -> Optional[ImageType]:
    response = requests.get(image_url)
    if response.status_code != 200:
        return

    return Image.open(io.BytesIO(response.content))


generators = {
    'news': generate_twitter_news_card,
}


@app.task
def update_twitter_card(post: dict) -> dict:
    text: str = post.get('title')
    image_url: str = post.get('feature_image')
    primary_tag: str = post.get('primary_tag', {}).get('slug')
    image: Optional[ImageType] = None

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
            'twitter_image': image_url,
        }
    ).json()
