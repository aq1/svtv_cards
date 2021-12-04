from PIL import Image

from ..layers.backgrounds import create_opinion_background_layer
from ..layers.headers import create_opinion_header_layer
from ..layers.titles import create_opinion_title_layer
from ..layers.footers import create_opinion_footer_layer

from ..compilers import compile_layers


def generate_opinion_card(post: dict, cover: Image.Image, profile_image: Image.Image):
    background: Image.Image = create_opinion_background_layer(
        cover=cover,
    )

    author: dict = post['primary_author'] or {}

    layers: list[Image.Image] = [
        create_opinion_header_layer(),
        create_opinion_title_layer(post.get('title', '')),
        create_opinion_footer_layer(
            name=author.get('name', ''),
            bio=author.get('bio', ''),
            profile_image=profile_image,
        )
    ]

    return compile_layers(
        background=background,
        layers=layers,
    )
