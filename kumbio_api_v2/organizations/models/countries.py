"""Countries model."""

# Django
from django.db import models
from slugify import slugify

# Models
from kumbio_api_v2.utils.models import KumbioModel


class Country(KumbioModel):
    name = models.CharField(max_length=255)
    slug_name = models.SlugField(max_length=255)
    phone_prefix = models.CharField(max_length=255)

    alpha_code = models.CharField(max_length=255)
    alpha_code1 = models.CharField(max_length=255)

    # Hour management
    timezone_raw = models.CharField(max_length=255, null=True, blank=True)
    minutes_diff = models.IntegerField(default=0)

    # phone rules
    max_length_phone = models.IntegerField(null=True, blank=True)
    min_length_phone = models.IntegerField(null=True, blank=True)

    optional_prefix = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Some countries prefix'
    )

    def save(self, *args, **kwargs):
        self.slug_name = slugify(self.name, separator="_")
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        """Meta class."""

        verbose_name_plural = "Países"
