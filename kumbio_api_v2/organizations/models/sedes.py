"""Headquarters model"""

# Django
from django.db import models

# Models
from kumbio_api_v2.utils.models import DaysChoices, KumbioModel


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


class HeadquarterSchedule(KumbioModel):
    """Headquarters schedule."""

    day = models.CharField(max_length=10, choices=DaysChoices.choices, default=DaysChoices.MONDAY)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name="sede_schedules")
    hour_init = models.TimeField()
    hour_end = models.TimeField()

    def __str__(self):
        """Return headquarter schedule."""
        return f"{self.day} schedule: {self.hour_init} - {self.hour_end}"

    class Meta:
        """Meta class."""

        verbose_name = "Horario de la sede"
        verbose_name_plural = "Horarios de las sedes"
