from django.db import models


class OnlineMessage(models.Model):

    chat_id = models.CharField(
        max_length=255,
    )

    message_service_id = models.CharField(
        max_length=255,
    )

    media_group_id = models.CharField(
        max_length=2055,
        default='',
    )

    title = models.CharField(
        max_length=2000,
        default='',
        blank=True,
    )

    ghost_id = models.CharField(
        max_length=255,
        default='',
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    text = models.TextField()
    html = models.TextField()

    def __str__(self):
        return f'{self.message_service_id}: {self.title}'
