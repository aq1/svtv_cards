from django.db import models


class RSSSource(models.Model):
    url = models.URLField(
        max_length=2048,
        unique=True,
    )

    last_updated_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return f'{self.url}'
