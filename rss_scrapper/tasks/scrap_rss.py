import datetime
from time import sleep, mktime

import feedparser
import telegram
from django.conf import settings

from ..models import RssFeed

MESSAGE_CHUNK_SIZE = 10


def scrap_rss():
    entries = []

    for source in RssFeed.objects.filter(is_active=True):
        feed_dict = feedparser.parse(source.url)
        published_at = None

        for entry in feed_dict['entries']:
            if not entry.get('published_parsed'):
                continue
            published_at = datetime.datetime.fromtimestamp(
                mktime(entry['published_parsed']),
            ).replace(
                microsecond=0,
                tzinfo=None,
            ).isoformat()

            if published_at <= source.last_updated_at:
                continue

            link = entry['link']
            title = entry['title']
            entries.append(
                f'<a href="{link}">{title}</a> - {source.name}'
            )

        if published_at:
            source.last_updated_at = published_at
            source.save()

    if not entries:
        return

    bot = telegram.Bot(token=settings.CHANNEL_BOT_TOKEN)

    for i in range(0, len(entries), MESSAGE_CHUNK_SIZE):
        try:
            bot.send_message(
                settings.RSS_FEED_CHANNEL_ID,
                text='\n\n'.join(entries[i:i + MESSAGE_CHUNK_SIZE]),
                parse_mode=telegram.ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except telegram.error.RetryAfter as e:
            sleep(e.retry_after)
        sleep(1)
