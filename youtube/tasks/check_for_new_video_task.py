import xml.etree.ElementTree as ET
from urllib.parse import (
    urlparse,
    parse_qs,
)

import requests
from django.conf import settings
from telegram import Bot

from cards.utils import download_image
from ghost.ghost_admin_request import (
    get_post,
    update_post,
    upload_image,
)

TASK_RETRY_COUNTDOWN = 5 * 60


def get_video_snippet(video_id: str):
    url = 'https://www.googleapis.com/youtube/v3/videos'
    response = requests.get(url, params={
        'part': 'snippet',
        'id': video_id,
        'key': settings.YOUTUBE_API_KEY,
    })

    response.raise_for_status()

    return response.json()['items'][0]['snippet']


def get_last_youtube_video():
    response = requests.get(f'https://www.youtube.com/feeds/videos.xml?channel_id={settings.YOUTUBE_CHANNEL_ID}')
    response.raise_for_status()
    tree = ET.fromstring(response.text)
    video = tree.find('{http://www.w3.org/2005/Atom}entry')
    video_id = video.find('{http://www.youtube.com/xml/schemas/2015}videoId').text
    return video_id, get_video_snippet(video_id)


def update_video_banner(post, video_id, snippet) -> None:
    cover = download_image(snippet['thumbnails']['medium']['url'])

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
            'title': snippet['title'],
        },
    )
    response.raise_for_status()


def notify(text):
    Bot(token=settings.TELEGRAM_TOKEN).send_message(
        settings.TELEGRAM_ADMIN_ID,
        text=text,
    )


def check_for_new_video():
    post: dict = get_post(post_id=settings.YOUTUBE_BANNER_POST_ID)
    try:
        current_video_id = parse_qs(urlparse(post['feature_image_caption']).query)['v'][0]
    except (KeyError, IndexError, ValueError):
        current_video_id = ''

    video_id, snippet = get_last_youtube_video()
    is_published = post['status'] == 'published'
    is_live = snippet['liveBroadcastContent'] in ('live', 'upcoming')
    is_same_id = current_video_id == video_id

    if is_live and is_published and is_same_id:
        return

    if not is_live and is_published:
        update_post(
            post_id=post['id'],
            post_updated_at=post['updated_at'],
            data={
                'status': 'draft',
            },
        )

        notify(f'Unpublished\n{snippet["title"]}\nhttps://youtube.com/watch?v={video_id}')
        return

    if is_live and not is_published:
        update_video_banner(
            post=post,
            video_id=video_id,
            snippet=snippet,
        )
        notify(f'Published\n{snippet["title"]}\nhttps://youtube.com/watch?v={video_id}')
        return
