from django.db import models


class OnlineMessage(models.Model):

    message_service_id = models.CharField(
        max_length=255,
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