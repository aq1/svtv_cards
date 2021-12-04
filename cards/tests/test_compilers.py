from cards.layers.backgrounds import create_news_background_layer
from cards.layers.backgrounds import create_thread_background_layer
from cards.layers.backgrounds import create_opinion_background_layer

from cards.layers.headers import create_news_header_layer
from cards.layers.headers import create_thread_header_layer
from cards.layers.headers import create_opinion_header_layer

from cards.layers.titles import create_news_title_layer
from cards.layers.titles import create_thread_title_layer
from cards.layers.titles import create_opinion_title_layer

from cards.layers.footers import create_opinion_footer_layer

from cards.compilers.compiler import compile_layers
from cards.tests.covers import (
    AUTHORS,
    COVERS,
)


def test_compiler():
    background = create_news_background_layer(
        cover=COVERS[0],
    )
    layers = [
        create_news_header_layer(),
        create_news_title_layer('VК возглавит сын Сергея Кириенко')
    ]

    compile_layers(
        background=background,
        layers=layers,
    ).show()

    background = create_thread_background_layer(
        cover=COVERS[1],
    )
    layers = [
        create_thread_header_layer(),
        create_thread_title_layer(f'Новость заголовок проверка_длинное_слово' * 2)
    ]

    compile_layers(
        background=background,
        layers=layers,
    ).show()

    background = create_opinion_background_layer(
        cover=COVERS[2],
    )
    layers = [
        create_opinion_header_layer(),
        create_opinion_title_layer(f'Новость заголовок проверка_длинное_слово' * 2),
        create_opinion_footer_layer(
            name='Малек Дудаков',
            bio='политолог, эксперт по политике США',
            profile_image=AUTHORS[0],
        )
    ]

    compile_layers(
        background=background,
        layers=layers,
    ).show()


test_compiler()
