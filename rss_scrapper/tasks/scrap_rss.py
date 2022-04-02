from time import sleep

import feedparser
import telegram
from django.conf import settings
from django.utils import timezone

from ..models import RSSSource

MESSAGE_CHUNK_SIZE = 5


def scrap_rss():
    entries = []

    for source in RSSSource.objects.filter(is_active=True):
        feed_dict = feedparser.parse(source.url)
        for entry in reversed(feed_dict['entries']):
            if entry['published_parsed'] <= source.last_updated_at.timetuple():
                continue

            entries.append(
                f"[{entry['title']}]({entry['link']}) - *{feed_dict['feed']['title']}*"
            )

        source.last_updated_at = timezone.now()
        source.save()

    if not entries:
        return

    bot = telegram.Bot(token=settings.CHANNEL_BOT_TOKEN)

    for i in range(0, len(entries), MESSAGE_CHUNK_SIZE):
        bot.send_message(
            settings.RSS_FEED_CHANNEL_ID,
            text='\n\n'.join(entries[i:i + MESSAGE_CHUNK_SIZE]),
            parse_mode=telegram.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
        sleep(1)
