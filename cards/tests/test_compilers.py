from pathlib import Path

from cards.layers.backgrounds import create_news_background_layer
from cards.layers.backgrounds import create_thread_background_layer
from cards.layers.backgrounds import create_opinion_background_layer
from cards.layers.backgrounds import create_translation_background_layer
from cards.layers.backgrounds import create_factchecking_background_layer
from cards.layers.backgrounds import create_test_background_layer

from cards.layers.headers import create_news_header_layer
from cards.layers.headers import create_thread_header_layer
from cards.layers.headers import create_opinion_header_layer
from cards.layers.headers import create_translation_header_layer
from cards.layers.headers import create_factchecking_header_layer
from cards.layers.headers import create_test_header_layer

from cards.layers.titles import create_news_title_layer
from cards.layers.titles import create_thread_title_layer
from cards.layers.titles import create_opinion_title_layer
from cards.layers.titles import create_factchecking_title_layer
from cards.layers.titles import create_test_title_layer

from cards.layers.footers import create_opinion_footer_layer

from cards.compilers.compiler import compile_layers
from cards.settings import FACTCHECKING_TAGS
from cards.tests.covers import (
    AUTHORS,
    COVERS,
    OPINION_COVERS,
)

RESULT_DIR = 'results'
Path(RESULT_DIR).mkdir(exist_ok=True)


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
    ).save(f'{RESULT_DIR}/news.jpg')


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
    ).save(f'{RESULT_DIR}/thread.jpg')


def test_opinion_compiler():
    titles = [
        'Как работают суды сегодня',
        'Правосудие над либеральным фантазёром',
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
        background = create_translation_background_layer(
            cover=cover,
        )
        layers = [
            create_translation_header_layer('cnn.com'),
            create_opinion_title_layer(title),
            create_opinion_footer_layer(**author),
        ]

        compile_layers(
            background=background,
            layers=layers,
        ).save(f'{RESULT_DIR}/o-{title}.jpg')


def test_factchecking_compiler():
    titles = (
        'Короткий фактчекинг из',
        'Средний фактчекинг из пары предложение, пара слов, еще',
        'Длинный фактчекинг из пары предложение, пара слов, еще Длинный фактчекинг',
        'Длинный фактчекинг из пары предложение, пара слов, еще Длинный фактчекинг еще Длинный фактчекинг',
        'Длинный фактчекинг из пары предложение, пара слов, еще Длинный фактчекинг еще Длинный фактчекинг',
        'Длинный фактчекинг из пары предложение, пара слов, еще Длинный фактчекинг еще Длинный фактчекинг еще Длинный фактчекинг',
        'В Беларуси США и страны НАТО осуществляют попытки свержения власти с'
        ' применением элементов гибридной войны  применением элементов гибридной войны  применением элементов гибридной войны '
    )

    author_name = 'Иван Иванов'
    date = 'написала в своем Телеграм-канале 3 декабря '

    for title, tag in zip(titles, FACTCHECKING_TAGS):
        background = create_factchecking_background_layer()
        layers = [
            create_factchecking_header_layer(),
            create_factchecking_title_layer(
                title=title,
                author_name=author_name,
                date=date,
                tag=tag,
            ),
        ]

        compile_layers(
            background=background,
            layers=layers,
        ).save(f'{RESULT_DIR}/f-{tag}.jpg')


def test_test_compiler():
    titles = (
        'На сколько лет вы сядете в либеральной России будущего?',
        'Одна строка',
    )

    from PIL import Image
    cover = Image.open('/Users/vladimirgrechukhin/Downloads/hCCGCL8zZYEezDs3TwLVv.jpeg')

    for title in titles:
        background = create_test_background_layer(
            cover=cover,
        )
        layers = [
            create_test_header_layer(),
            create_test_title_layer(
                title=title,
                tag='тест',
            ),
        ]

        compile_layers(
            background=background,
            layers=layers,
        ).save(f'{RESULT_DIR}/t-{title}.jpg')


def test_result_compiler():
    titles = (
        'Вы совсем не разбираетесь в новогодней гастрономии',
        'Вы совсем немножко разбираетесь в новогодней гастрономии',
        'Вы разбираетесь в новогодней гастрономии!',
        'Поздравляем, Вы — новогодний гастрономический эксперт!',
    )

    covers = (
        '/Users/vladimirgrechukhin/Downloads/photo_2021-12-30 13.43.50.jpeg',
        '/Users/vladimirgrechukhin/Downloads/photo_2021-12-30 13.43.52.jpeg',
        '/Users/vladimirgrechukhin/Downloads/photo_2021-12-30 13.43.54.jpeg',
        '/Users/vladimirgrechukhin/Downloads/photo_2021-12-30 13.43.55 (1).jpeg',
    )

    from PIL import Image
    for i, title, cover in zip(range(4), titles, covers):
        background = create_test_background_layer(
            cover=Image.open(cover),
        )
        layers = [
            create_test_header_layer(),
            create_test_title_layer(
                title=title,
            ),
        ]

        compile_layers(
            background=background,
            layers=layers,
        ).save(f'{RESULT_DIR}/r-{i}.jpg')


def test_compilers():
    test_news_compiler()
    test_threads_compiler()
    test_opinion_compiler()
    test_factchecking_compiler()
    test_test_compiler()


if __name__ == '__main__':
    test_news_compiler()
