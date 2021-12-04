from PIL import Image

from .generic_background_layer import create_generic_background_layer
from ...assets import open_image


def create_news_background_layer(cover: Image.Image) -> Image.Image:
    tail = open_image(
        name='news-tail.png',
    )

    return create_generic_background_layer(cover=cover, tail=tail)
