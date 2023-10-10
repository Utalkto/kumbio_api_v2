# Django
from django.db import models

# Models
from kumbio_api_v2.utils.models import KumbioModel


class Sector(KumbioModel):
    """Organization sectors."""

    name = models.CharField(max_length=100)
    description = models.TextField()
    default_image = models.ImageField(
        upload_to='organizations',
        default=None,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectores'

    def __str__(self) -> str:
        return f'{self.name}'
