from PIL import (
    Image,
)

from ...assets import (
    open_image,
)
from ...settings import (
    TEST_HEADER_SIZE,
    LEFT_PADDING,
    HEADER_HEIGHT,
)


def create_test_header_layer() -> Image.Image:
    header = Image.new('RGBA', TEST_HEADER_SIZE, (0, 0, 0, 0))
    logo = open_image('logo.png')
    header.alpha_composite(logo, (LEFT_PADDING, HEADER_HEIGHT - logo.height))
    return header
