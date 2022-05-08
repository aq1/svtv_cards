from PIL import Image

from ghost.ghost_api_request import get_post
from ..layers.backgrounds import create_opinion_background_layer
from ..layers.headers import create_opinion_header_layer
from ..layers.titles import create_opinion_title_layer
from ..layers.footers import create_opinion_footer_layer

from ..compilers import compile_layers
from ..utils import download_image


def generate_opinion_card(post: dict):
    # на вебхук приходит пост без информации об авторах
    post: dict = get_post(
        post_id=post['id'],
        include=['authors'],
    )

    background: Image.Image = create_opinion_background_layer(
        cover=download_image(post.get('feature_image')),
    )

    layers: list[Image.Image] = [
        create_opinion_header_layer(),
        create_opinion_title_layer(post.get('title', '')),
        create_opinion_footer_layer(post['authors']),
    ]

    return compile_layers(
        background=background,
        layers=layers,
    )
