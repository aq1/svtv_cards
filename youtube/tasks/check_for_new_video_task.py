import xml.etree.ElementTree as ET
from urllib.parse import (
    urlparse,
    parse_qs,
)

import celery
from django.conf import settings
import requests

from cards.utils import download_image
from project.celery import app
from ghost.ghost_admin_request import (
    get_post,
    update_post,
    upload_image,
)

TASK_RETRY_COUNTDOWN = 5 * 60


def get_last_youtube_video() -> tuple[str, str, str]:
    response = requests.get(f'https://www.youtube.com/feeds/videos.xml?channel_id={settings.YOUTUBE_CHANNEL_ID}')
    response.raise_for_status()
    tree = ET.fromstring(response.text)
    video = tree.find('{http://www.w3.org/2005/Atom}entry')
    video_id = video.find('{http://www.youtube.com/xml/schemas/2015}videoId').text
    cover_url = video.find('{http://search.yahoo.com/mrss/}group/{http://search.yahoo.com/mrss/}thumbnail').attrib[
        'url']
    title = video.find('{http://www.w3.org/2005/Atom}title').text
    return video_id, cover_url, title


def update_video_banner(post: dict, video_id: str, cover_url: str, title: str) -> None:
    cover = download_image(cover_url)

    response = upload_image(
        image_name=f'{post["id"]}_youtube_banner.jpeg',
        image=cover,
    )

    response.raise_for_status()

    response = update_post(
        post_id=post['id'],
        post_updated_at=post['updated_at'],
        data={
            'status': 'published',
            'feature_image': response.json()['images'][0]['url'],
            'feature_image_caption': f'https://www.youtube.com/watch?v={video_id}',
            'title': title,
        },
    )
    response.raise_for_status()


@app.task(bind=True)
def check_for_new_video(self: celery.Task) -> None:
    # не хочу настраивать celery beat, поэтому пусть таска будет вызывать себя бесконечно
    post: dict = get_post(post_id=settings.YOUTUBE_BANNER_POST_ID)
    try:
        current_video_id = parse_qs(urlparse(post['feature_image_caption']).query)['v'][0]
    except (KeyError, IndexError, ValueError):
        current_video_id = ''

    video_id, cover_url, title = get_last_youtube_video()
    if video_id != current_video_id:
        update_video_banner(
            post=post,
            video_id=video_id,
            cover_url=cover_url,
            title=title,
        )

    self.apply_async(countdown=TASK_RETRY_COUNTDOWN)
