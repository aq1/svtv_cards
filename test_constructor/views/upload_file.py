from io import BytesIO

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ghost.ghost_admin_request import upload_image
from PIL import Image


@csrf_exempt
def upload_file(request):
    _file = request.FILES['image']
    name = _file.name
    image = Image.open(_file.file)

    if not _file.name.endswith('.gif'):
        f = BytesIO()
        image.convert('RGB').save(f, format='jpeg')
        image = Image.open(f)
        name = '.'.join(_file.name.split('.')[:-1]) + '.jpeg'

    r = upload_image(name, image)
    url = r.json()['images'][0]['url']
    if not url.startswith('http'):
        url = f'https://svtv.org{url}'

    response = {
        'success': 1,
        'file': {
            'url': url,
        }
    }
    return JsonResponse(
        response,
        status=201,
    )
