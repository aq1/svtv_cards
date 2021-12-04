from .generic_title_layer import create_generic_title_layer
from ...settings import (
    OPINION_TITLE_SIZE,
    OPINION_TITLE_SPACING,
    OPINION_TITLE_LAYER_HEIGHT,
    OPINION_TITLE_WIDTH,
    OPINION_TITLE_MAX_LINES,
    TITLE_FILL,
)


def create_opinion_title_layer(title):
    return create_generic_title_layer(
        title=title,
        font_size=OPINION_TITLE_SIZE,
        font_spacing=OPINION_TITLE_SPACING,
        title_fill=TITLE_FILL,
        layer_height=OPINION_TITLE_LAYER_HEIGHT,
        title_width=OPINION_TITLE_WIDTH,
        title_max_lines=OPINION_TITLE_MAX_LINES,
    )
