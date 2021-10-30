from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def ghost_webhook_view(request):
    if request.GET.get('key') != settings.WEBHOOK_KEY:
        return HttpResponse(status=400)

    return HttpResponse('Okay')
