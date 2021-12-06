from PIL import Image

from .generic_background_layer import create_generic_background_layer
from ...assets import open_image
from ...settings import (
    CARD_SIZE,
)


def create_factchecking_background_layer() -> Image.Image:
    tail = open_image(
        name='factchecking-tail.png',
    )

    cover = Image.new('RGBA', CARD_SIZE, 0)

    return create_generic_background_layer(cover=cover, tail=tail)
