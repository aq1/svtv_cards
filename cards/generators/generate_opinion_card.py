from PIL import Image

from ..layers.backgrounds import create_opinion_background_layer
from ..layers.headers import create_opinion_header_layer
from ..layers.titles import create_opinion_title_layer
from ..layers.footers import create_opinion_footer_layer

from ..compilers import compile_layers
from ..utils import download_image


def generate_opinion_card(post: dict):
    background: Image.Image = create_opinion_background_layer(
        cover=download_image(post.get('feature_image')),
    )

    author: dict = post['primary_author'] or {}

    layers: list[Image.Image] = [
        create_opinion_header_layer(),
        create_opinion_title_layer(post.get('title', '')),
        create_opinion_footer_layer(
            name=author.get('name', ''),
            bio=author.get('bio', ''),
            profile_image=download_image(author.get('profile_image')),
        )
    ]

    return compile_layers(
        background=background,
        layers=layers,
    )
