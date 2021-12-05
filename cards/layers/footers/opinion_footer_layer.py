from PIL import (
    Image,
    ImageDraw,
)

from ...assets import open_font
from ...settings import (
    FOOTER_SIZE,
    LEFT_PADDING,
    OPINION_PROFILE_IMAGE_SIZE,
    OPINION_NAME_COORDS,
    OPINION_NAME_FONT_SIZE,
    OPINION_BIO_COORDS,
    OPINION_BIO_FONT_SIZE,
    OPINION_BIO_FILL,
    TITLE_FILL,
)


def create_circle_profile_image(profile_image: Image.Image) -> Image.Image:
    profile_image = profile_image.resize(OPINION_PROFILE_IMAGE_SIZE).convert('RGBA')
    profile_image_circle = Image.new('L', OPINION_PROFILE_IMAGE_SIZE, 0)
    draw = ImageDraw.Draw(profile_image_circle)
    # минус один пиксель, потому что иначе круг обрезается неровно
    draw.ellipse((0, 0, OPINION_PROFILE_IMAGE_SIZE[0] - 1, OPINION_PROFILE_IMAGE_SIZE[1] - 1), fill=255)
    profile_image.putalpha(profile_image_circle)

    return profile_image


def create_opinion_footer_layer(name: str, bio: str, profile_image: Image.Image) -> Image.Image:
    layer: Image.Image = Image.new('RGBA', FOOTER_SIZE)
    profile_image: Image.Image = create_circle_profile_image(profile_image)

    layer.alpha_composite(profile_image, (LEFT_PADDING, 0))

    draw = ImageDraw.Draw(layer)
    draw.text(
        OPINION_NAME_COORDS,
        name,
        font=open_font('Roboto-Medium.ttf', OPINION_NAME_FONT_SIZE),
        fill=TITLE_FILL,
    )

    draw.text(
        OPINION_BIO_COORDS,
        bio,
        font=open_font('Roboto-Regular.ttf', OPINION_BIO_FONT_SIZE),
        fill=OPINION_BIO_FILL,
    )

    return layer
