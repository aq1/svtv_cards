from .generic_header_layer import create_generic_header_layer
from ...settings import (
    FACTCHECKING_TAG_FILL,
    FACTCHECKING_TAG_SIZE,
)


def create_factchecking_header_layer():
    return create_generic_header_layer(
        tag='Фактчекинг',
        tag_fill=FACTCHECKING_TAG_FILL,
        tag_size=FACTCHECKING_TAG_SIZE,
    )
