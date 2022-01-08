import json

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from ghost.ghost_admin_request import get_post
from ghost.ghost_admin_request import update_post
from ghost.ghost_admin_request import create_post
from ..models import Test


@csrf_exempt
def save_test(request):
    test = json.loads(request.body.decode('utf8'))

    if not test['general']['id']:
        ghost_post = create_post(test['general']['title'])
        test['general']['id'] = ghost_post['id']
        test['general']['url'] = ghost_post['url']

    test_model, _ = Test.objects.get_or_create(
        id=test['general']['id'],
    )

    test_model.json = json.dumps(test, ensure_ascii=False)
    test_model.save()

    test_html = render_to_string('test_constructor/test_template.html', context={'test': test})

    ghost_post = get_post(test['general']['id'])
    update_post(
        post_id=ghost_post['id'],
        post_updated_at=ghost_post['updated_at'],
        data={
            'title': test['general']['title'],
            'feature_image': test['general']['cover'],
            'html': test_html,
            'tags': [{'name': 'Тест'}],
            'codeinjection_foot': '<script src="/assets/built/js/test2.js"></script>',
        },
    )

    return JsonResponse(
        data={
            'id': test['general']['id'],
            'url': test['general']['url'],
        },
        status=201,
    )
