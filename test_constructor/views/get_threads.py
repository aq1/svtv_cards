from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Thread


@csrf_exempt
def get_threads(request):

    tests = [t.json for t in Thread.objects.all()]

    return JsonResponse(
        data={
            'threads': tests,
        },
    )
