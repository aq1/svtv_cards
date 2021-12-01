from PIL.Image import Image

from .generate_card import generate_card


def generate_thread_card(text: str, image: Image) -> Image:
    return generate_card(
        text=text,
        image=image,
        tag='Тред',
        tag_color=(247, 147, 26),
        tail='threads/thread-tail.png',
    )
