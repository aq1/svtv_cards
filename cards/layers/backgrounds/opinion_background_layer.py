from typing import Optional

from PIL import Image

from .generic_background_layer import create_generic_background_layer
from ...assets import (
    open_image,
)
from ...settings import (
    OPINION_COVER_OPACITY,
)


def create_opinion_background_layer(cover: Optional[Image.Image] = None) -> Image.Image:
    tail = open_image(
        name='opinion-tail.png',
    )

    return create_generic_background_layer(
        cover=cover,
        tail=tail,
        cover_opacity=OPINION_COVER_OPACITY,
    )
