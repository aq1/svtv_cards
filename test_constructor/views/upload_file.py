from io import BytesIO

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ghost.ghost_admin_request import upload_image
from PIL import Image


@csrf_exempt
def upload_file(request):
    _file = request.FILES['image']
    image = Image.open(_file.file).convert('RGB')
    f = BytesIO()
    image.save(f, format='jpeg')
    image = Image.open(f)
    name = '.'.join(_file.name.split('.')[:-1]) + '.jpeg'
    r = upload_image(name, image)
    return HttpResponse(
        r.json()['images'][0]['url'],
        status=201,
    )
