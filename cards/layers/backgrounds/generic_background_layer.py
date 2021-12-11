from typing import Optional

from PIL import Image

from ...settings import (
    CARD_BACKGROUND_FILL,
    COVER_OPACITY,
    CARD_SIZE,
)


def create_generic_background_layer(
        tail: Image.Image,
        cover: Optional[Image.Image] = None,
        cover_opacity: Optional[float] = COVER_OPACITY,
) -> Image.Image:
    background = Image.new('RGBA', CARD_SIZE, CARD_BACKGROUND_FILL)

    if cover:
        coef = max(background.width / cover.width, background.height / cover.height)
        new_size = int(cover.width * coef), int(cover.height * coef)
        image = cover.resize(new_size).convert('RGBA')
        image.putalpha(int(cover_opacity * 255))
        background.alpha_composite(image)

    background.alpha_composite(tail, (0, background.height - tail.height))

    return background
