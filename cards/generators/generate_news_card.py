from PIL.Image import Image

from .generate_card import generate_card
from .settings import NEWS_TAG_FILL


def generate_news_card(text: str, image: Image, **_) -> Image:
    return generate_card(
        text=text,
        image=image,
        tag='Новость',
        tag_color=NEWS_TAG_FILL,
        tail='news/news-tail.png',
    )
