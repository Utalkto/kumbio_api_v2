"""Headquarters model"""

# Django
from django.db import models
from django.db.models import Q

# Models
from kumbio_api_v2.utils.models import DaysChoices, KumbioModel

# Rest Framework
from rest_framework.exceptions import ValidationError

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
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name="sede_schedule")
    hour_init = models.TimeField()
    hour_end = models.TimeField()
    is_working = models.BooleanField(default=True)
    note = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        """Return headquarter schedule."""
        return f"{self.day} schedule: {self.hour_init} - {self.hour_end}"

    class Meta:
        """Meta class."""

        verbose_name = "Horario de la sede"
        verbose_name_plural = "Horarios de las sedes"
        unique_together = (("sede", "day", "hour_init"), ("sede", "day", "hour_end"))

    def save(self, *args, **kwargs):
        self.check_schedules_overlapping()
        schedule = super().save(*args, **kwargs)
        return schedule

    def check_schedules_overlapping(self):
        overlapping_schedules = HeadquarterSchedule.objects.filter(
            Q(# Valida si el nuevo horario se superpone con un horario existente desde afuera o es exactamente el mismo: Existente  | |
                hour_init__gt=self.hour_init,                                                                         # Nuevo     |     |
                hour_end__lt=self.hour_end
            ) | Q( # Valida si el inicio del nuevo horario se superpone con un horario existente desde adentro: Existente |   |
                hour_init__lt=self.hour_init,                                                                 # Nuevo      |    |
                hour_end__gt=self.hour_init
            ) | Q( # Valida si el final del nuevo horario se superpone con un horario existente desde adentro: Existente      |   |
                hour_init__lt=self.hour_end,                                                                 # Nuevo       |     |
                hour_end__gt=self.hour_end
            ),
            sede=self.sede,
            day=self.day
        ).exists()
        if overlapping_schedules:
            raise ValidationError("El horario que estas intentando crear se esta sobreponiendo con otro horario")
        return overlapping_schedules
