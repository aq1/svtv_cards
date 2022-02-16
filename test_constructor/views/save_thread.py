import json

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from ghost.ghost_admin_request import create_post
from ghost.ghost_admin_request import get_post
from ghost.ghost_admin_request import update_post
from ..models import Thread

'''
const getWord = function (count) {
    "use strict";
    count = Math.abs(count) % 100;
    const n1 = count % 10;

    if (count > 10 && count < 20) {
        return 'карточек';
    }
    if (n1 > 1 && n1 < 5) {
        return 'карточки';
    }
    if (n1 === 1) {
        return 'карточка';
    }
    return 'карточек';
};
'''


def get_word(count):
    count = abs(count) % 100
    n1 = count % 10

    if 10 < count < 20:
        return 'карточек'

    if 1 < n1 < 5:
        return 'карточки'

    if n1 == 1:
        return 'карточка'

    return 'карточек'


@csrf_exempt
def save_thread(request):
    thread = json.loads(request.body.decode('utf8'))

    if not thread['general']['id']:
        ghost_post = create_post(thread['general']['title'])
        thread['general']['id'] = ghost_post['id']
        thread['general']['url'] = ghost_post['url']

    for card in thread['cards']:
        card.pop('isActive', None)

    thread_model, _ = Thread.objects.get_or_create(
        id=thread['general']['id'],
    )

    thread_model.json = json.dumps(thread, ensure_ascii=False)
    thread_model.save()

    thread_html = render_to_string('test_constructor/thread_template.html', context={'thread': thread})

    ghost_post = get_post(thread['general']['id'])
    cards_count = len(thread['cards'])
    post_response = update_post(
        post_id=ghost_post['id'],
        post_updated_at=ghost_post['updated_at'],
        data={
            'title': thread['general']['title'],
            'slug': thread['general']['slug'],
            'feature_image': thread['general']['cover'],
            'html': thread_html,
            'tags': [{'name': 'Тред'}],
            'authors': ['ruvalerydz@gmail.com'],
            'custom_excerpt': f'{cards_count} {get_word(cards_count)}'
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
