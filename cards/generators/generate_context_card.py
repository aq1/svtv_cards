from PIL import Image

from ..compilers import compile_layers
from ..layers.backgrounds import create_news_background_layer
from ..layers.footers import create_context_footer_layer
from ..layers.headers.generic_header_layer import create_generic_header_layer
from ..layers.titles import create_news_title_layer
from ..layers.titles.generic_title_layer import create_generic_title_layer
from ..settings import NEWS_TAG_FILL, DEFAULT_TAG_SIZE, TITLE_SIZE, TITLE_SPACING, TITLE_FILL, \
    OPINION_TITLE_LAYER_HEIGHT
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
        create_generic_title_layer(
            title=post.get('title', ''),
            layer_height=OPINION_TITLE_LAYER_HEIGHT,
            font_size=TITLE_SIZE,
            font_spacing=TITLE_SPACING,
            title_fill=TITLE_FILL,
        ),
        create_context_footer_layer(
            excerpt=post['excerpt'],
        ),
    ]

    return compile_layers(
        background=background,
        layers=layers,
    )
