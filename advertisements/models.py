from django.conf import settings
from django.db import models


class AdvertisementStatusChoices(models.TextChoices):
    OPEN = 'OPEN', 'Открыто'
    CLOSED = 'CLOSED', 'Закрыто'


class Advertisement(models.Model):
    title = models.TextField()
    description = models.TextField(default='')
    status = models.CharField(
        choices=AdvertisementStatusChoices.choices,
        max_length=10,
        default=AdvertisementStatusChoices.OPEN,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='advertisements',
    )

    def __str__(self):
        return self.title