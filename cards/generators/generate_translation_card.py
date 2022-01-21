from PIL import Image

from ghost.ghost_api_request import get_post
from ..layers.backgrounds import create_translation_background_layer
from ..layers.headers import create_translation_header_layer
from ..layers.titles import create_opinion_title_layer
from ..layers.footers import create_opinion_footer_layer

from ..compilers import compile_layers
from ..utils import download_image


def generate_translation_card(post: dict):

    # на вебхук приодит пост без информации об авторах
    post: dict = get_post(
        post_id=post['id'],
        include=['authors'],
    )

    background: Image.Image = create_translation_background_layer(
        cover=download_image(post.get('feature_image')),
    )

    author: dict = post['primary_author'] or {}

    layers: list[Image.Image] = [
        create_translation_header_layer(
            additional_text=post['feature_image_alt'],
        ),
        create_opinion_title_layer(post.get('title', '')),
        create_opinion_footer_layer(
            name=author.get('name', ''),
            bio=author.get('bio', ''),
            profile_image=download_image(author.get('profile_image')),
        ),
    ]

    return compile_layers(
        background=background,
        layers=layers,
    )
