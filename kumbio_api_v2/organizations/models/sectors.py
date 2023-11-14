# Django
from django.db import models
from slugify import slugify

# Models
from kumbio_api_v2.utils.models import KumbioModel


class Sector(KumbioModel):
    """Sector model."""

    name = models.CharField(max_length=100)
    description = models.TextField()
    default_image = models.ImageField(upload_to="organizations", default=None, null=True, blank=True)

    class Meta:
        verbose_name = "Sector"
        verbose_name_plural = "Sectores"

    def __str__(self):
        return f"{self.name}"


class SubSector(KumbioModel):
    """Sub sectors model."""

    name = models.CharField(max_length=100)
    slug_name = models.SlugField(unique=True, max_length=100, blank=True, null=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name="sub_sectors")

    def save(self, *args, **kwargs):
        if not self.slug_name:
            self.slug_name = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Sub Sector"
        verbose_name_plural = "Sub Sectores"

    def __str__(self):
        return f"{self.name}"


# class SectorProfileHealth(KumbioModel):
#     """Sector  health profile model."""

#     class BloodType(models.TextChoices):
#         """
#         Types of files.
#         """
#         A = 'A', 'A'
#         B = 'B', 'B'
#         AB = 'AB', 'AB'
#         O = 'O', 'O'


#     sub_sector = models.ForeignKey(SubSector, on_delete=models.CASCADE, related_name="sub_sectors_profile")
#     blood_type = models.TextField("Tipo de sangre")
#     initial_weight = models.FloatField("Peso inicial")
#     initial_height = models.FloatField("Altura inicial")
