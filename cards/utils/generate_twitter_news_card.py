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

TEXT_WIDTH = 35
TEXT_MAX_LINES = 5
TEXT_PLACEHOLDER = '...'

TEXT_COORDINATES = (60, 48)
TEXT_FILL = (255, 255, 255, 255)

TEXT_BACKGROUND_COORDINATES = (0, 220)
LOGO_COORDINATES = (60, 84)

IMAGE_RATIO = 0.65


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
    gradient = open_image('gradient.png')
    ratio = (IMAGE_RATIO * background.width) / image.width
    image = image.convert('RGBA').resize((int(image.width * ratio), int(image.height * ratio)))
    image.alpha_composite(gradient, (0, 0))
    coords = (background.width - image.width, 0)
    background.alpha_composite(image, coords)


def generate_twitter_news_card(text: str, image: ImageType) -> ImageType:
    background = open_image('news/background.png')
    text_background = open_image('news/text-background.png')
    logo = open_image('logo.png')
    font = open_font()

    text = '\n'.join(
        textwrap.wrap(
            text,
            width=TEXT_WIDTH,
            max_lines=TEXT_MAX_LINES,
            placeholder=TEXT_PLACEHOLDER,
        )
    )

    draw = ImageDraw.Draw(text_background)
    draw.multiline_text(
        TEXT_COORDINATES,
        text,
        font=font,
        fill=TEXT_FILL,
        spacing=FONT_SPACING,
    )

    if image:
        add_image_to_card(background, image)

    background.alpha_composite(text_background, TEXT_BACKGROUND_COORDINATES)
    background.alpha_composite(logo, LOGO_COORDINATES)

    return background.convert('RGB')
