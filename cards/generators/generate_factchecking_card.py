from PIL import Image

from ..layers.backgrounds import create_factchecking_background_layer
from ..layers.headers import create_factchecking_header_layer
from ..layers.titles import create_factchecking_title_layer

from ..compilers import compile_layers


def generate_thread_card(post: dict) -> Image.Image:
    background: Image.Image = create_factchecking_background_layer()

    layers: list[Image.Image] = [
        create_factchecking_header_layer(),
        create_factchecking_title_layer(
            title=post.get('title'),
            author_name='',
            date='',
            truth_level='',
        ),
    ]

    return compile_layers(
        background=background,
        layers=layers,
    )
