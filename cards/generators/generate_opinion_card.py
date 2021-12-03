from typing import Optional

from PIL.Image import Image as ImageType
from PIL import Image

from ..utils import download_image

from .generate_card import generate_card
from .settings import (
    CARD_BACKGROUND_FILL,
    OPINION_TAG_FILL,
    FOOTER_SIZE,
    RIGHT_PADDING,
)


def generate_opinion_footer(name: str, bio: str, image_url: str) -> ImageType:
    footer = Image.new('RGBA', FOOTER_SIZE, CARD_BACKGROUND_FILL)

    if image_url:
        profile_image: Optional[ImageType] = download_image(image_url)
        if profile_image:
            profile_image = profile_image.resize(120, 120)
            footer.alpha_composite(profile_image, (RIGHT_PADDING, 0))

    return footer


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
