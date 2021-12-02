import textwrap
from typing import Optional

from PIL import (
    Image,
    ImageFont,
    ImageDraw,
)
from PIL.Image import Image as ImageType
from PIL.ImageFont import FreeTypeFont
from django.conf import settings

from .settings import (
    FONT_SIZE,
    TAG_FONT_SIZE,
    FONT_SPACING,
    TEXT_WIDTH,
    TEXT_MAX_LINES,
    TEXT_PLACEHOLDER,
    RIGHT_PADDING,
    TEXT_FILL,
    LOGO_COORDINATES,
    COVER_OPACITY,
)


def open_image(name: str) -> ImageType:
    return Image.open(
        str(settings.IMAGES_DIR / 'images' / name)
    )


def open_font(font_name, size) -> FreeTypeFont:
    return ImageFont.truetype(
        str(settings.IMAGES_DIR / 'fonts' / font_name),
        size=size,
    )


def add_image_to_card(background: ImageType, image: ImageType):
    coef = max(background.width / image.width, background.height / image.height)
    new_size = int(image.width * coef), int(image.height * coef)
    image = image.resize(new_size).convert('RGBA')
    image.putalpha(int(COVER_OPACITY * 255))
    background.alpha_composite(image)


def generate_card(
        text: str,
        image: ImageType,
        tag: str,
        tag_color: tuple[int, int, int],
        tail: str,
        footer: Optional[ImageType] = None,
) -> ImageType:
    background = open_image('background.png')
    logo = open_image('logo.png')
    tail = open_image(tail)
    text_font = open_font('Roboto-Medium.ttf', FONT_SIZE)
    tag_font = open_font('Roboto-Bold.ttf', TAG_FONT_SIZE)

    text = textwrap.wrap(
        text,
        width=TEXT_WIDTH,
        max_lines=TEXT_MAX_LINES,
        placeholder=TEXT_PLACEHOLDER,
    )

    text_height = FONT_SIZE * len(text) + FONT_SPACING * len(text) - 1

    # посередине между лого и низом
    text_y_coord = int(
        (LOGO_COORDINATES[1] + logo.height + background.height - text_height) / 2
    )

    text = '\n'.join(text)

    if image:
        add_image_to_card(background, image)

    background.alpha_composite(tail, (0, background.height - tail.height))

    draw = ImageDraw.Draw(background)
    draw.multiline_text(
        (RIGHT_PADDING, text_y_coord),
        text,
        font=text_font,
        fill=TEXT_FILL,
        spacing=FONT_SPACING,
    )

    draw.multiline_text(
        (RIGHT_PADDING, LOGO_COORDINATES[1]),
        tag.upper(),
        font=tag_font,
        fill=tag_color,
    )

    background.alpha_composite(logo, LOGO_COORDINATES)

    if footer:
        background.alpha_composite(footer, (0, background.width - footer.width))

    return background.convert('RGB')
