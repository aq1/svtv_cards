from typing import Optional

import requests

from django.conf import settings


def make_ghost_request(
        method: str,
        path: str,
        files: Optional[dict] = None,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
) -> requests.Response:
    params = params or {}
    params['key'] = settings.GHOST_API_KEY

    request = requests.Request(
        method=method,
        url=f'{settings.GHOST_URL}/ghost/api/v4/content/{path}',
        files=files,
        data=data,
        json=json,
        headers=headers,
        params=params,
    ).prepare()

    return requests.Session().send(request)


def get_post(post_id: str, include: Optional[list[str]] = None):
    response = make_ghost_request(
        'get',
        f'posts/{post_id}/',
        params={
            'include': include,
        },
    )

    if response.status_code != 200:
        return

    try:
        return response.json().get('posts')[0]
    except (KeyError, IndexError):
        return
