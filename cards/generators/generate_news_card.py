from PIL import Image

from ..layers.backgrounds import create_news_background_layer
from ..layers.headers import create_news_header_layer
from ..layers.titles import create_news_title_layer

from ..compilers import compile_layers


def generate_news_card(post: dict, cover: Image.Image) -> Image.Image:
    background: Image.Image = create_news_background_layer(
        cover=cover,
    )

    layers: list[Image.Image] = [
        create_news_header_layer(),
        create_news_title_layer(post.get('title', '')),
    ]

    return compile_layers(
        background=background,
        layers=layers,
    )
