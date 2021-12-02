from PIL.Image import Image

from .generate_card import generate_card

from .settings import THREAD_TAG_FILL


def generate_thread_card(text: str, image: Image, **_) -> Image:
    return generate_card(
        text=text,
        image=image,
        tag='Тред',
        tag_color=THREAD_TAG_FILL,
        tail='threads/thread-tail.png',
    )
