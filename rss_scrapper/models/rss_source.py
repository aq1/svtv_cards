from django.db import models
from django.utils import timezone


def now():
    return timezone.now().isoformat()


class RssFeed(models.Model):

    name = models.CharField(
        max_length=255,
        default='',
    )

    url = models.URLField(
        max_length=2048,
        unique=True,
    )

    last_updated_at = models.CharField(
        max_length=255,
        default=now,
    )

    is_active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return f'{self.url}'
