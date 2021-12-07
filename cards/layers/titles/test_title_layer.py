import textwrap

from PIL import (
    Image,
    ImageDraw,
)

from ...assets import open_font
from ...settings import (
    TITLE_SIZE,
    TITLE_SPACING,
    TITLE_FILL,
    LEFT_PADDING,
    CARD_WIDTH,
    CARD_HEIGHT,
    TITLE_WIDTH,
    TEST_TITLE_MAX_LINES,
    TITLE_PLACEHOLDER,
    TEST_HEADER_HEIGHT,
    TEST_TAG_FILL,
    DEFAULT_TAG_SIZE,
)


def create_test_title_layer(title: str) -> Image.Image:
    layer = Image.new('RGBA', (CARD_WIDTH, CARD_HEIGHT - TEST_HEADER_HEIGHT))

    font = open_font('Roboto-Medium.ttf', TITLE_SIZE)
    title = textwrap.wrap(
        title,
        width=TITLE_WIDTH,
        max_lines=TEST_TITLE_MAX_LINES,
        placeholder=TITLE_PLACEHOLDER,
    )

    title_height = TITLE_SIZE * len(title) + TITLE_SPACING * (len(title) - 1)

    text_y_coord = layer.height - (title_height + TITLE_SIZE)

    title = '\n'.join(title)

    draw = ImageDraw.Draw(layer)
    draw.multiline_text(
        (LEFT_PADDING, text_y_coord),
        title,
        font=font,
        fill=TITLE_FILL,
        spacing=TITLE_SPACING,
    )

    tag_y_coord = text_y_coord - (DEFAULT_TAG_SIZE + TITLE_SPACING)

    font = open_font('Roboto-Bold.ttf', DEFAULT_TAG_SIZE)
    draw = ImageDraw.Draw(layer)
    draw.multiline_text(
        (LEFT_PADDING, tag_y_coord),
        'ТЕСТ',
        font=font,
        fill=TEST_TAG_FILL,
    )

    return layer
