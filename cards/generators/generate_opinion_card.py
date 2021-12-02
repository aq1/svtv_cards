from typing import Optional

from PIL.Image import Image

from ..utils import download_image

from .generate_card import generate_card
from .settings import OPINION_TAG_FILL


def generate_opinion_footer(name: str, bio: str, image_url: str) -> Image:
    profile_image: Optional[Image] = None

    if image_url:
        profile_image = download_image(image_url)


def generate_opinion_card(text: str, image: Image, author: dict, **_) -> Image:
    opinion_footer = generate_opinion_footer(
        name=author.get('name', ''),
        bio=author.get('bio', ''),
        image_url=author.get('profile_image', ''),
    )

    return generate_card(
        text=text,
        image=image,
        tag='Мнение',
        tag_color=OPINION_TAG_FILL,
        tail='news/opinion-tail.png',
        footer=opinion_footer,
    )
