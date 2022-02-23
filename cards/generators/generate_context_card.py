from PIL import Image

from ..compilers import compile_layers
from ..layers.backgrounds import create_news_background_layer
from ..layers.headers.generic_header_layer import create_generic_header_layer
from ..layers.titles import create_news_title_layer
from ..settings import NEWS_TAG_FILL, DEFAULT_TAG_SIZE
from ..utils import download_image


def generate_context_card(post: dict) -> Image.Image:
    background: Image.Image = create_news_background_layer(
        cover=download_image(post.get('feature_image')),
    )

    layers: list[Image.Image] = [
        create_generic_header_layer(
            tag='Контекст',
            tag_fill=NEWS_TAG_FILL,
            tag_size=DEFAULT_TAG_SIZE,
        ),
        create_news_title_layer(post.get('title', '')),
    ]

    return compile_layers(
        background=background,
        layers=layers,
    )
