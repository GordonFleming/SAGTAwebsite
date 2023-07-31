from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class MapDownload(models.Model):
    download_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Download Date',
        help_text='The date and time when the map was downloaded.'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='downloads',
        verbose_name='User',
        help_text='The user who downloaded the map.'
    )

    downloaded_map = models.CharField(
        max_length=200,
        verbose_name='Downloaded Map',
        help_text='The name or identifier of the downloaded map.',
        blank=True,
        default=''
    )

    def __str__(self):
        return (
            f'{self.downloaded_map} downloaded by '
            f'{self.user.username} on {self.download_date}'
        )
