from PIL.Image import Image

from .generate_card import generate_card


def generate_twitter_card(text: str, image: Image) -> Image:
    return generate_card(
        text=text,
        image=image,
        tag='Новость',
        tag_color=(254, 210, 122),
        tail='news/news-tail.png',
    )
