from PIL import Image

from ghost.ghost_api_request import get_post
from ..layers.backgrounds import create_factchecking_background_layer
from ..layers.headers import create_factchecking_header_layer
from ..layers.titles import create_factchecking_title_layer

from ..compilers import compile_layers
from ..settings import FACTCHECKING_TAGS


def generate_factchecking_card(post: dict) -> Image.Image:

    post: dict = get_post(post['id'], include=['tags'])
    tag: str = ''

    for post_tag in post.get('tags', []):
        if post_tag in FACTCHECKING_TAGS:
            tag = post_tag['slug']

    if not tag:
        raise ValueError(f'Tag was not found in factchecking post\n{post["tags"]}')

    background: Image.Image = create_factchecking_background_layer()
    layers: list[Image.Image] = [
        create_factchecking_header_layer(),
        create_factchecking_title_layer(
            title=post.get('title'),
            author_name=post.get('feature_image_caption'),
            date=post.get('feature_image_alt'),
            tag=tag,
        ),
    ]

    return compile_layers(
        background=background,
        layers=layers,
    )
