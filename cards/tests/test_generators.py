from cards.generators import generate_news_card
from cards.generators import generate_thread_card
from cards.tests.covers import COVERS


def test_generators():
    post = {
        'title': 'Заголовок для карточки',
    }

    generate_news_card(post, COVERS[0]).show()
    generate_thread_card(post, COVERS[2]).show()


test_generators()
