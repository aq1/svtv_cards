from django.db import models


class OnlineAttachment(models.Model):

    message = models.ForeignKey(
        'online.OnlineMessage',
        on_delete=models.CASCADE,
    )

    attachment_id = models.CharField(
        max_length=255,
    )

    url = models.CharField(
        max_length=255,
    )

    meta = models.TextField()

    def __str__(self):
        return f'{self.message}: {self.url}'
