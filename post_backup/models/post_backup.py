from django.db import models
from simple_history.models import HistoricalRecords


class PostBackup(models.Model):

    ghost_id = models.CharField(
        max_length=255,
    )

    title = models.CharField(
        max_length=2048,
        default='',
    )

    post = models.JSONField(
        default=dict,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    history = HistoricalRecords()

    def __str__(self):
        return f'Post {self.ghost_id}'
