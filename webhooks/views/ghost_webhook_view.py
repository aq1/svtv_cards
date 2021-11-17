import json
from functools import wraps

from django.conf import settings
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


def ghost_webhook_view(view):
    @wraps(view)
    @csrf_exempt
    @require_http_methods(['POST'])
    def _f(request, *args, **kwargs):
        if request.GET.get('key') != settings.WEBHOOK_KEY:
            return HttpResponse(status=400)

        body = json.loads(request.body)
        post = body['post']['current']
        previous = body['post'].get('previous', {})
        return view(request, post, previous)

    return _f
