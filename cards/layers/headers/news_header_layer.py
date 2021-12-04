from .generic_header_layer import create_generic_header_layer
from ...settings import (
    NEWS_TAG_FILL,
    DEFAULT_TAG_SIZE,
)


def create_news_header_layer():
    return create_generic_header_layer(
        tag='Тред',
        tag_fill=NEWS_TAG_FILL,
        tag_size=DEFAULT_TAG_SIZE,
    )
