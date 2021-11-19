import textwrap

from PIL import (
    Image,
    ImageFont,
    ImageDraw,
)
from PIL.Image import Image as ImageType
from PIL.ImageFont import FreeTypeFont
from django.conf import settings

FONT_SIZE = 58
FONT_SPACING = 14

TEXT_WIDTH = 33
TEXT_MAX_LINES = 4
TEXT_PLACEHOLDER = '...'

RIGHT_PADDING = 60
TEXT_FILL = (255, 255, 255, 255)

LOGO_Y_COORDINATE = 84

COVER_OPACITY = 0.35


def open_image(name: str) -> ImageType:
    return Image.open(
        str(settings.IMAGES_DIR / 'images' / name)
    )


def open_font() -> FreeTypeFont:
    return ImageFont.truetype(
        str(settings.IMAGES_DIR / 'fonts' / 'Roboto-Medium.ttf'),
        size=FONT_SIZE,
    )


def add_image_to_card(background: ImageType, image: ImageType):
    coef = max(background.width / image.width, background.height / image.height)
    new_size = int(image.width * coef), int(image.height * coef)
    image = image.resize(new_size)
    image.putalpha(int(COVER_OPACITY * 255))
    background.alpha_composite(image)


def generate_twitter_news_card(text: str, image: ImageType) -> ImageType:
    background = open_image('news/background.png')
    logo = open_image('logo.png')
    font = open_font()

    text = textwrap.wrap(
        text,
        width=TEXT_WIDTH,
        max_lines=TEXT_MAX_LINES,
        placeholder=TEXT_PLACEHOLDER,
    )

    text_height = FONT_SIZE * len(text) + FONT_SPACING * len(text) - 1

    # посередине между лого и низом
    text_y_coord = int(
        (LOGO_Y_COORDINATE + logo.height + background.height - text_height) / 2
    )

    text = '\n'.join(text)

    if image:
        add_image_to_card(background, image)

    draw = ImageDraw.Draw(background)
    draw.multiline_text(
        (RIGHT_PADDING, text_y_coord),
        text,
        font=font,
        fill=TEXT_FILL,
        spacing=FONT_SPACING,
    )

    background.alpha_composite(logo, (RIGHT_PADDING, LOGO_Y_COORDINATE))

    return background.convert('RGB')
