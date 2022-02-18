import io
from datetime import datetime
from typing import Any, Optional

import jwt as jwt
import requests
from PIL.Image import Image

from django.conf import settings


def get_token():
    # https://ghost.org/docs/admin-api/#token-authentication

    admin_id, admin_key = settings.GHOST_ADMIN_KEY.split(':')
    iat = int(datetime.now().timestamp())
    header = {'alg': 'HS256', 'typ': 'JWT', 'kid': admin_id}
    payload = {
        'iat': iat,
        'exp': iat + 5 * 60,
        'aud': '/v4/admin/'
    }

    return jwt.encode(payload, bytes.fromhex(admin_key), algorithm='HS256', headers=header)


def make_ghost_request(
        method: str,
        path: str,
        files: Optional[dict] = None,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
) -> requests.Response:
    headers = headers or {}
    headers['Authorization'] = f'Ghost {get_token()}'

    request = requests.Request(
        method=method,
        url=f'{settings.GHOST_URL}/ghost/api/v4/admin{path}',
        files=files,
        data=data,
        json=json,
        headers=headers,
    ).prepare()

    return requests.Session().send(request)


def upload_image(image_name: str, image: Image) -> requests.Response:
    _file = io.BytesIO()
    is_gif = image_name.endswith('gif')
    _format = 'gif' if is_gif else 'jpeg'
    image.save(_file, format=_format, save_all=is_gif)
    _file.seek(0)

    files = {
        'file': (
            image_name,
            _file,
            'image/jpeg',
            {'Content-Type': 'multipart/form-data;'},
        ),
    }

    return make_ghost_request(
        'post',
        '/images/upload/',
        files=files,
        data={'ref': image_name},
    )


def update_post(post_id: str, post_updated_at: str, data: dict[str, Any]) -> requests.Response:
    data.update({
        'updated_at': post_updated_at,
    })

    return make_ghost_request(
        'put',
        f'/posts/{post_id}?source=html',
        json={
            'posts': [data],
        },
    )


def get_post(post_id: Optional[str] = '', post_slug: Optional[str] = '') -> dict:
    url = f'/posts/{post_id}'
    if post_slug:
        url = f'/posts/slug/{post_slug}'

    response = make_ghost_request(
        'get',
        url,
    )

    return response.json()['posts'][0]


def get_page(page_id: Optional[str] = '', page_slug: Optional[str] = '') -> dict:
    url = f'/pages/{page_id}'
    if page_slug:
        url = f'/pages/slug/{page_slug}'

    response = make_ghost_request(
        'get',
        url,
    )

    return response.json()['pages'][0]


def create_post(title: str) -> dict:
    response = make_ghost_request(
        'post',
        '/posts/?source=html',
        json={
            'posts': [{
                'title': title,
            }]
        },
    )
    return response.json()['posts'][0]


def create_page(title: str) -> dict:
    response = make_ghost_request(
        'post',
        '/pages/?source=html',
        json={
            'pages': [{
                'title': title,
            }]
        },
    )
    return response.json()['pages'][0]


def update_page(page_id: str, page_updated_at: str, data: dict[str, Any]) -> requests.Response:
    data.update({
        'updated_at': page_updated_at,
    })

    return make_ghost_request(
        'put',
        f'/pages/{page_id}?source=html',
        json={
            'pages': [data],
        },
    )
