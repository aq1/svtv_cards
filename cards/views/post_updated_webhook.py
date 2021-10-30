import json
from functools import wraps

from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from ..utils import update_twitter_card


def key_required(view):
    @wraps(view)
    def _f(request, *args, **kwargs):
        if request.GET.get('key') != settings.WEBHOOK_KEY:
            return HttpResponse(status=400)
        return view(request, *args, **kwargs)

    return _f


@csrf_exempt
@require_http_methods(['POST'])
@key_required
def post_updated_webhook(request: HttpRequest) -> HttpResponse:
    body = json.loads(request.body)
    post = body['post']['current']
    previous = body['post'].get('previous', {})

    fields_to_watch = [
        'title',
        'feature_image',
        'status',
    ]

    if not any([r in previous for r in fields_to_watch]):
        return HttpResponse(status=202)

    update_twitter_card.delay(post)

    return HttpResponse()
