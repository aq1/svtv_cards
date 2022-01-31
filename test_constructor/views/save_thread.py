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
from ..models import Thread


@csrf_exempt
def save_thread(request):
    thread = json.loads(request.body.decode('utf8'))

    if not thread['general']['id']:
        ghost_post = create_post(thread['general']['title'])
        thread['general']['id'] = ghost_post['id']
        thread['general']['url'] = ghost_post['url']

    thread_model, _ = Thread.objects.get_or_create(
        id=thread['general']['id'],
    )

    thread_model.json = json.dumps(thread, ensure_ascii=False)
    thread_model.save()

    thread_html = render_to_string('test_constructor/thread_template.html', context={'thread': thread})

    ghost_post = get_post(thread['general']['id'])
    post_response = update_post(
        post_id=ghost_post['id'],
        post_updated_at=ghost_post['updated_at'],
        data={
            'title': thread['general']['title'],
            'slug': thread['general']['slug'],
            'feature_image': thread['general']['cover'],
            'html': thread_html,
            'tags': [{'name': 'Тред'}],
        },
    )

    if post_response.status_code != 200:
        return JsonResponse(
            data=post_response.json(),
            status=400,
        )

    return JsonResponse(
        data={
            'id': thread['general']['id'],
            'url': thread['general']['url'],
        },
        status=201,
    )
