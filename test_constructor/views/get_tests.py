from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Test


@csrf_exempt
def get_tests(request):

    tests = [t.json for t in Test.objects.all()]

    return JsonResponse(
        data={
            'tests': tests,
        },
    )
