from django.db import models


class Test(models.Model):

    id = models.CharField(
        primary_key=True,
        max_length=1000,
    )

    json = models.TextField()

    def __str__(self):
        return f'Test {self.id}'
