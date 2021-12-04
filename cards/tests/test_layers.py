from cards.layers.backgrounds import create_news_background_layer
from cards.layers.backgrounds import create_thread_background_layer
from cards.layers.backgrounds import create_opinion_background_layer

from cards.layers.headers import create_news_header_layer
from cards.layers.headers import create_opinion_header_layer
from cards.layers.headers import create_thread_header_layer

from cards.layers.titles import create_news_title_layer
from cards.layers.titles import create_thread_title_layer
from cards.layers.titles import create_opinion_title_layer

from cards.layers.footers import create_opinion_footer_layer

from cards.tests.covers import (
    AUTHORS,
    COVERS,
)


def test_background():
    create_news_background_layer(COVERS[0]).show()
    create_thread_background_layer(COVERS[1]).show()
    create_opinion_background_layer(COVERS[2]).show()


def test_headers():
    create_news_header_layer().show()
    create_thread_header_layer().show()
    create_opinion_header_layer().show()


def test_titles():
    lines = [
        'Заголовок в одну строку',
        'Заголовок в две строки Заголовок в две строки',
        'Заголовок в три строки Заголовок в три строки Заголовок в три строки',
        'Заголовок в четыре строки Заголовок в четыре строки Заголовок в четыре строки Заголовок в четыре строки',
        (
            'Заголовок который обрежется Заголовок который обрежется '
            'Заголовок который обрежется Заголовок который обрежется Заголовок который обрежется '
        ),
    ]

    for line in lines:
        # create_news_title_layer(line).show()
        # create_thread_title_layer(line).show()
        create_opinion_title_layer(line).show()


def test_footers():
    for author in AUTHORS:
        create_opinion_footer_layer(
            name='Малек Дудаков',
            bio='политолог, эксперт по политике США',
            profile_image=author,
        ).show()

    create_opinion_footer_layer(
        name='Малек Дудаков',
        bio='политолог, эксперт по политике США',
        profile_image=COVERS[1],
    ).show()


# test_background()
# test_headers()
# test_titles()
test_footers()
