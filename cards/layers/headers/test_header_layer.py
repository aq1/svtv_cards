from PIL import (
    Image,
    ImageDraw,
)

from ...assets import (
    open_image,
    open_font,
)
from ...settings import (
    TEST_HEADER_HEIGHT,
    TEST_HEADER_SIZE,
    LEFT_PADDING,
    HEADER_HEIGHT,
    TEST_TAG_FILL,
    DEFAULT_TAG_SIZE,
)


def create_test_header_layer() -> Image.Image:
    header = Image.new('RGBA', TEST_HEADER_SIZE, (0, 0, 0, 0))
    logo = open_image('logo.png')
    header.alpha_composite(logo, (LEFT_PADDING, HEADER_HEIGHT - logo.height))

    font = open_font('Roboto-Bold.ttf', DEFAULT_TAG_SIZE)
    draw = ImageDraw.Draw(header)
    draw.multiline_text(
        (LEFT_PADDING, TEST_HEADER_HEIGHT - DEFAULT_TAG_SIZE),
        'ТЕСТ',
        font=font,
        fill=TEST_TAG_FILL,
    )
    return header
