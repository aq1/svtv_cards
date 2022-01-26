import json

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from ghost.ghost_admin_request import get_post
from ghost.ghost_admin_request import get_page
from ghost.ghost_admin_request import update_post
from ghost.ghost_admin_request import update_page
from ghost.ghost_admin_request import create_post
from ghost.ghost_admin_request import create_page
from ..models import Test


def get_redirect_script_for_share_page(url):
    return '''
        <script>
            window.location.replace(`${window.location.protocol}//${window.location.host}/test/%s/`)
        </script>
    ''' % url


def get_result_html(url):
    return f'''
    <!doctype html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <title></title>
        </head>
        <body>
        <div id="url" data-url="{url}"></div>
        <script src="/assets/built/js/testResult.js?v=2"></script>
        </body>
        </html>
    '''


def generate_result_picture(title, image):
    from cards.layers.backgrounds import create_test_background_layer
    from cards.layers.headers import create_test_header_layer
    from cards.layers.titles import create_test_title_layer
    from cards.compilers import compile_layers
    from ghost.ghost_admin_request import upload_image

    import requests
    from PIL import Image

    background = create_test_background_layer(
        cover=Image.open(requests.get(image).content),
    )

    layers: list = [
        create_test_header_layer(),
        create_test_title_layer(
            title=title,
        ),
    ]

    cover = compile_layers(
        background=background,
        layers=layers,
    )

    return upload_image(
        f'{title}.jpg',
        cover,
    ).json()['images'][0]['url']


@csrf_exempt
def save_test(request):
    test = json.loads(request.body.decode('utf8'))

    if not test['general']['id']:
        ghost_post = create_post(test['general']['title'])
        test['general']['id'] = ghost_post['id']
        test['general']['url'] = ghost_post['url']

    for result in test['results']:
        if not result['shareUrl']:
            continue

        try:
            page = get_page(
                page_slug=result['shareUrl'],
            )
        except KeyError:
            page = create_page(
                title=f'Шеринг теста: {result["header"]}',
            )

        twitter_image = None
        if result['image']:
            twitter_image = generate_result_picture(result['header'], result['image'])

        response = update_page(
            page_id=page['id'],
            page_updated_at=page['updated_at'],
            data={
                'slug': result['shareUrl'],
                'feature_image': result['image'],
                'meta_title': result['header'],
                'meta_description': f'{result["header"]} - проверьте по ссылке',
                'twitter_image': twitter_image,
                'html': get_result_html(test['general']['url']),
            },
        )

    test_model, _ = Test.objects.get_or_create(
        id=test['general']['id'],
    )

    test_model.json = json.dumps(test, ensure_ascii=False)
    test_model.save()

    test_html = render_to_string('test_constructor/test_template.html', context={'test': test})

    ghost_post = get_post(test['general']['id'])
    post_response = update_post(
        post_id=ghost_post['id'],
        post_updated_at=ghost_post['updated_at'],
        data={
            'title': test['general']['title'],
            'slug': test['general']['slug'],
            'feature_image': test['general']['cover'],
            'html': test_html,
            'tags': [{'name': 'Тест'}, {'name': '#АвтоТест'}],
        },
    )

    return JsonResponse(
        data={
            'id': test['general']['id'],
            'url': test['general']['url'],
        },
        status=201,
    )
