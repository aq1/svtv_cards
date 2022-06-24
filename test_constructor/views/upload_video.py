from io import BytesIO

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ghost.ghost_admin_request import upload_image
from online.tasks.upload_file import upload_file as upload_file_to_s3
from PIL import Image


@csrf_exempt
def upload_video(request):
    _file = request.FILES['image']
    name = _file.name

    url = upload_file_to_s3(name, _file, _file.content_type)
    if not url.startswith('http'):
        url = f'https://svtv.org{url}'

    response = {
        'success': 1,
        'file': {
            'url': url,
            'title': name,
        }
    }
    return JsonResponse(
        response,
        status=201,
    )
