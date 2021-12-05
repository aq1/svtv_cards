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
    OPINION_COVERS,
)


def test_news_compiler():
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


def test_threads_compiler():
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


def test_opinion_compiler():
    titles = [
        'Как работают суды сегодня',
        'Реквием по Рашагейту',
        'Как политика пришла в видеоигры',
        'Триумвират Германии',
        'Новое мение с длинным заголовком. Таким длинным что он даже не умещается в три строки.',
    ]

    authors = [
        {
            'name': 'Родион Белькович',
            'bio': 'Политолог, историк, республиканец',
            'profile_image': AUTHORS[0],
        },
        {
            'name': 'Малек Дудаков',
            'bio': 'Политолог, эксперт по политике США',
            'profile_image': AUTHORS[1],
        },
        {
            'name': 'Сергей Цилюрик',
            'bio': 'Игровой публицист',
            'profile_image': AUTHORS[2],
        },
        {
            'name': 'Юджин Август',
            'bio': 'Член Гражданского Общества, публицист',
            'profile_image': AUTHORS[3],
        },
        {
            'name': 'Новый автор',
            'bio': 'С аватаркой, которая не является кружочком с прозрачным фоном',
            'profile_image': AUTHORS[4],
        },
    ]

    covers = OPINION_COVERS + COVERS[:1]

    for cover, title, author in zip(covers, titles, authors):
        background = create_opinion_background_layer(
            cover=cover,
        )
        layers = [
            create_opinion_header_layer(),
            create_opinion_title_layer(title),
            create_opinion_footer_layer(**author),
        ]

        compile_layers(
            background=background,
            layers=layers,
        ).save(f'{title}.jpg')


def test_compilers():
    # test_news_compiler()
    # test_threads_compiler()
    test_opinion_compiler()


test_compilers()
