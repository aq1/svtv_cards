import datetime
import re

import requests
import time
from html import escape

from config import tgstat_token as token

endpoint = "https://api.tgstat.ru"
usage_stat = endpoint + "/usage/stat?token={token}"
posts_search = endpoint + "/posts/search" \
           "?token={token}&q={q}&startDate={start_date}" \
           "&endDate={end_date}&minusWords={minus_words}" \
           "&extended=1&hideForwards={hide_forwards}" \
           "&hideDeleted={hide_deleted}&peerType={peer_type}" \
           "&limit=50"


emoji_media_types = {
    'mediaDocument': '📄 ',
    'mediaWebPage': '🌐 ',
    'mediaPhoto': '🖼 ',
    'mediaGeo': '🌍 ',
    'mediaContact': '☎️ ',
    'mediaVenue': '🎇 ',
    'mediaGeoLive': '🛺 ',
    'mediaGame': '🎮 ',
    'mediaInvoice': '💸 ',
    'mediaPoll': '📊 ',
    "video/mp4": '📹 ',
}


def fetch_posts_by_word(word: str, minus_words: str,
                        blacklist_ids: list, hide_forwards=True,
                        hide_deleted=True, peer_type='channel', interval=12000):
    end_date = int(time.time())
    start_date = end_date - interval
    resp = requests.get(posts_search.format(
        token=token,
        q=word,
        start_date=start_date,
        end_date=end_date,
        hide_forwards=int(hide_forwards),
        hide_deleted=int(hide_deleted),
        peer_type=peer_type,
        minus_words=minus_words
    ))
    if not resp:
        raise Exception("Some error with api or query")
    resp = resp.json()
    if resp.get("status") != "ok":
        raise Exception(f"Query status is not ok {resp}")
    items = resp["response"]['items']
    channels = resp["response"]["channels"]
    if int(resp['response']['total_count']) == 0:
        return ''
    answer = f"Найдено результатов по слову <i>{escape(word)}</i>: <b>{resp['response']['total_count']}</b>\n"
    for item in items:
        if [x for x in channels if -1000000000000 - x['tg_id'] in blacklist_ids and x['id'] == item['channel_id']]:
            continue
        if "/c/" in item["link"]:
            continue
        emoji = '•'
        if item.get("media") and item["media"].get("media_type"):
            emoji = '• ' + emoji_media_types[item["media"]["media_type"]]
            if item['media'].get("mime_type") in emoji_media_types:
                emoji = '• ' + emoji_media_types[item['media']["mime_type"]]
        clean_text = ' '.join(
            x for x in re.split(r'(?:\n|(<[^<>]+>))', item['text']) if x and (x[0] != '<' or x[-1] != '>')
        )
        answer += f"\n{emoji} {escape(clean_text[:69])}" \
                  f"{'...' if len(clean_text) > 69 else ''}" \
                  f"\n{item.get('media', {}).get('media_type', 'no media type')}\n" \
                  f"\n<a href='https://{item['link']}'>link</a>"
    return answer


def check_status():
    resp = requests.get(usage_stat.format(token=token))
    if not resp:
        raise Exception("Some error with api or query")
    resp = resp.json()
    if resp['status'] == 'ok':
        status = 'Подписка активна.'
    else:
        return 'Подписка неактивна!'
    title = f'Название тарифа: <strong>{resp["response"][0]["title"]}</strong>'
    spent_words = f'Использовано слов: <strong>{resp["response"][0]["spentWords"]}</strong>'
    spent_requests = f'Использовано запросов: <strong>{resp["response"][0]["spentRequests"]}</strong>'
    data_end = f'Срок действия подписки: <strong>{datetime.datetime.fromtimestamp(resp["response"][0]["expiredAt"])}</strong>'
    text = f"{status}\n{title}\n{spent_words}\n{spent_requests}\n{data_end}"
    return text
