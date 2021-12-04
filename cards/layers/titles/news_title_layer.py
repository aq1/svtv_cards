from PIL import Image

from .generic_title_layer import create_generic_title_layer
from ...settings import (
    TITLE_SIZE,
    TITLE_SPACING,
    TITLE_FILL,
)


def create_news_title_layer(title: str) -> Image.Image:
    return create_generic_title_layer(
        title=title,
        font_size=TITLE_SIZE,
        font_spacing=TITLE_SPACING,
        title_fill=TITLE_FILL,
    )
