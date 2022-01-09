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

        response = update_page(
            page_id=page['id'],
            page_updated_at=page['updated_at'],
            data={
                'slug': result['shareUrl'],
                'feature_image': result['image'],
                'codeinjection_head': get_redirect_script_for_share_page(test['general']['slug']),
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
