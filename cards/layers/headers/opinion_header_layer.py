from .generic_header_layer import create_generic_header_layer
from ...settings import (
    OPINION_TAG_FILL,
    OPINION_TAG_SIZE,
)


def create_opinion_header_layer():
    return create_generic_header_layer(
        tag='Мнение',
        tag_fill=OPINION_TAG_FILL,
        tag_size=OPINION_TAG_SIZE,
    )
