from .generic_header_layer import create_generic_header_layer
from ...settings import (
    TRANSLATION_TAG_FILL,
    OPINION_TAG_SIZE,
)


def create_translation_header_layer(additional_text: str):
    return create_generic_header_layer(
        tag='Перевод',
        additional_text=additional_text,
        tag_fill=TRANSLATION_TAG_FILL,
        tag_size=OPINION_TAG_SIZE,
    )
