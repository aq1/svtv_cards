from PIL import (
    Image,
    ImageDraw,
)

from ...assets import open_font
from ...settings import (
    FOOTER_SIZE,
    LEFT_PADDING,
    OPINION_PROFILE_IMAGE_SIZE,
    OPINION_NAME_FONT_SIZE,
    OPINION_BIO_FONT_SIZE,
    OPINION_BIO_FILL,
    TITLE_FILL,
    OPINION_PROFILE_IMAGE_WIDTH, OPINION_NAME_COORDS, OPINION_BIO_COORDS,
)
from ...utils import download_image


def create_circle_profile_image(profile_images: list[Image.Image]) -> list[Image.Image]:
    images = []
    for profile_image in profile_images:
        profile_image = profile_image.resize(OPINION_PROFILE_IMAGE_SIZE).convert('RGBA')
        profile_image_circle = Image.new('L', OPINION_PROFILE_IMAGE_SIZE, 0)
        draw = ImageDraw.Draw(profile_image_circle)
        # минус один пиксель, потому что иначе круг обрезается неровно
        draw.ellipse((0, 0, OPINION_PROFILE_IMAGE_SIZE[0] - 1, OPINION_PROFILE_IMAGE_SIZE[1] - 1), fill=255)
        profile_image.putalpha(profile_image_circle)
        images.append(profile_image)

    return images


def create_opinion_footer_layer(authors: list) -> Image.Image:
    layer = Image.new('RGBA', FOOTER_SIZE)
    print([a['profile_image'] for a in authors])
    profile_images = create_circle_profile_image(
        [download_image(a.get('profile_image')) for a in authors]
    )

    offset = 0
    step = int(OPINION_PROFILE_IMAGE_WIDTH * 0.7)
    for i, image in enumerate(profile_images, 0):
        layer.alpha_composite(image, (LEFT_PADDING + offset, 0))
        offset += step

    authors_title = [[]]
    for a in authors:
        if ', '.join(authors_title[-1]) + a['name'] > 35:
            authors_title.append([])
        authors_title[-1].append(a['name'])

    authors_title = '\n'.join([', '.join(a) for a in authors_title])

    draw = ImageDraw.Draw(layer)
    draw.text(
        (OPINION_NAME_COORDS[0] + offset - step, OPINION_NAME_COORDS[1]),
        authors_title,
        font=open_font('Roboto-Medium.ttf', OPINION_NAME_FONT_SIZE),
        fill=TITLE_FILL,
    )

    bio = ''
    if len(authors) == 1:
        bio = authors[0].get('bio') or ''

    draw.text(
        OPINION_BIO_COORDS,
        bio,
        font=open_font('Roboto-Regular.ttf', OPINION_BIO_FONT_SIZE),
        fill=OPINION_BIO_FILL,
    )

    return layer
