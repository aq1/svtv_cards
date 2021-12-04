from PIL import Image, ImageDraw

from ...assets import (
    open_font,
    open_image,
)

from ...settings import (
    HEADER_SIZE,
    HEADER_HEIGHT,
    LEFT_PADDING,
    TAG_Y_POSITION,
    LOGO_X_POSITION,
)


def create_generic_header_layer(tag: str, tag_fill: tuple[int, int, int], tag_size: int) -> Image.Image:
    header = Image.new('RGBA', HEADER_SIZE, (0, 0, 0, 0))

    font = open_font('Roboto-Bold.ttf', tag_size)
    logo = open_image('logo.png')

    draw = ImageDraw.Draw(header)
    draw.multiline_text(
        (LEFT_PADDING, TAG_Y_POSITION - tag_size),
        tag.upper(),
        font=font,
        fill=tag_fill,
    )

    header.alpha_composite(logo, (LOGO_X_POSITION, HEADER_HEIGHT - logo.height))

    return header
