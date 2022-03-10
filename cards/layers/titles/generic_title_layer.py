import textwrap
from typing import Optional

from PIL import Image, ImageDraw

from ...assets import open_font
from ...settings import (
    CARD_WIDTH,
    TITLE_LAYER_HEIGHT,
    TITLE_WIDTH,
    TITLE_MAX_LINES,
    TITLE_PLACEHOLDER, LEFT_PADDING,
)


def create_generic_title_layer(
        title: str,
        font_size: int,
        font_spacing: int,
        title_fill: tuple[int, int, int],
        layer_height: Optional[int] = TITLE_LAYER_HEIGHT,
        title_width: Optional[int] = TITLE_WIDTH,
        title_max_lines: Optional[int] = TITLE_MAX_LINES,
) -> Image.Image:
    layer = Image.new('RGBA', (CARD_WIDTH, layer_height))

    font = open_font('charterc-bold.woff', font_size)
    title = textwrap.wrap(
        title,
        width=title_width,
        max_lines=title_max_lines,
        placeholder=TITLE_PLACEHOLDER,
    )

    title_height = font_size * len(title) + font_spacing * (len(title) - 1)

    # посередине между лого и низом
    text_y_coord = int(
        (layer_height - title_height) / 2
    )

    title = '\n'.join(title)

    draw = ImageDraw.Draw(layer)
    draw.multiline_text(
        (LEFT_PADDING, text_y_coord),
        title,
        font=font,
        fill=title_fill,
        spacing=font_spacing,
    )
    return layer
