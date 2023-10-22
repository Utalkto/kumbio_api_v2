from django.db import models

from kumbio_api_v2.utils.models import KumbioModel


class Sede(KumbioModel):
    """Sede model."""

    class SedeTypeOptions(models.TextChoices):
        """Sede type options."""

        PHYSICAL = "PHYSICAL", "Física"
        VIRTUAL = "VIRTUAL", "Virtual"
        DOMICILE = "DOMICILE", "Domicilio"

    name = models.CharField(max_length=255)

    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE, related_name="organization_sedes"
    )
    description = models.TextField(null=True, blank=True)
    sede_type = models.CharField(max_length=10, choices=SedeTypeOptions.choices, default=SedeTypeOptions.PHYSICAL)
    address = models.CharField(max_length=255)
    maps_url = models.URLField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    phone_aux = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        """Meta class."""

        verbose_name = "Sede"
        verbose_name_plural = "Sedes"

    def __str__(self):
        return f"Sede {self.name} - {self.organization}"
