from PIL import Image

from ...assets import open_image
from ...settings import (
    CARD_SIZE,
)


def create_test_background_layer(cover: Image.Image) -> Image.Image:
    cover = cover.convert('RGBA')
    gradient = open_image('test_left_gradient.png')
    cover.thumbnail(CARD_SIZE)
    cover.alpha_composite(gradient, (0, 0))
    return cover
