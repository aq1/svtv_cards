from PIL import Image

from ..layers.backgrounds import create_test_background_layer
from ..layers.headers import create_test_header_layer
from ..layers.titles import create_test_title_layer

from ..compilers import compile_layers
from ..utils import download_image


def generate_test_card(post: dict) -> Image.Image:
    background: Image.Image = create_test_background_layer(
        cover=download_image(post.get('feature_image')),
    )

    layers: list[Image.Image] = [
        create_test_header_layer(),
        create_test_title_layer(post.get('title', '')),
    ]

    return compile_layers(
        background=background,
        layers=layers,
    )
