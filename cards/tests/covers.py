from cards.assets import open_image


def open_test_images(*images: str):
    return [
        open_image(f'test_images/{image}')
        for image in images
    ]


COVERS = open_test_images(
    'background_default.jpeg',
    'background_1x1.jpeg',
    'background_2.jpeg',
    'background_vertical.jpeg',
)

AUTHORS = open_test_images(
    'author_1.png',
    'author_2.png',
    'author_3.png',
    'author_4.png',
    'author_not_circle.jpeg',
)

OPINION_COVERS = open_test_images(
    'opinion_back_1.jpeg',
    'opinion_back_2.jpeg',
    'opinion_back_3.jpeg',
    'opinion_back_4.jpeg',
)

TEST_COVERS = open_test_images(
    'test_cover_1.png',
)
