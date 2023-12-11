# Django
from django.db import models
from django.db.models import Q

# Custom
from kumbio_api_v2.utils.models import DaysChoices, KumbioModel

# Rest Framework
from rest_framework.exceptions import ValidationError


class Professional(KumbioModel):
    """Professional model."""

    user = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name="professional")
    description = models.TextField(max_length=255, blank=True, null=True)
    sede = models.ForeignKey("organizations.Sede", on_delete=models.CASCADE, related_name="organization_professionals")
    services = models.ManyToManyField("organizations.Service", related_name="service_professionals")

    @property
    def organization(self):
        return self.sede.organization

    class Meta:
        """Meta class."""

        verbose_name = "Professional"
        verbose_name_plural = "Professionals"

    def __str__(self):
        return f"Professional {self.user.email} - {self.sede.name}"

    def check_has_service(self, service_pk):
        return self.services.filter(pk=service_pk).exists()


class ProfessionalSchedule(KumbioModel):
    """Professional schedule."""

    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name="professional_schedule")
    day = models.CharField(max_length=10, choices=DaysChoices.choices, default=DaysChoices.MONDAY)
    hour_init = models.TimeField()
    hour_end = models.TimeField()
    is_working = models.BooleanField(default=True)
    note = models.TextField(max_length=255, blank=True, null=True)

    class Meta:
        """Meta class."""

        verbose_name = "Professional Schedule"
        verbose_name_plural = "Professional Schedules"
        unique_together = (("professional", "day", "hour_init"), ("professional", "day", "hour_end"))

    def __str__(self):
        return f"Schedule {self.professional} - {self.day}"

    def save(self, *args, **kwargs):
        self.check_schedules_overlapping()
        schedule = super().save(*args, **kwargs)
        return schedule

    def check_schedules_overlapping(self):
        overlapping_schedules = ProfessionalSchedule.objects.filter(
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
            professional=self.professional,
            day=self.day
        ).exists()
        if overlapping_schedules:
            raise ValidationError("El horario que estas intentando crear se esta sobreponiendo con otro horario")
        return overlapping_schedules


class RestProfessionalSchedule(KumbioModel):
    """Rest professional schedule."""

    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name="rest_professional_schedule")
    date_init = models.DateField()
    date_end = models.DateField()
    description = models.TextField(max_length=255, blank=True, null=True)

    class Meta:
        """Meta class."""

        verbose_name = "Rest Professional Schedule"
        verbose_name_plural = "Rest Professional Schedules"
        unique_together = (("professional", "date_init"), ("professional", "date_end"))

    def __str__(self):
        return f"Rest Professional Schedule {self.professional}"

    def save(self, *args, **kwargs):
        self.check_schedules_overlapping()
        schedule = super().save(*args, **kwargs)
        return schedule

    def check_schedules_overlapping(self):
        overlapping_schedules = RestProfessionalSchedule.objects.filter(
            Q(# Valida si el nuevo horario se superpone con un horario existente desde afuera o es exactamente el mismo: Existente  | |
                date_init__gt=self.date_init,                                                                         # Nuevo     |     |
                date_end__lt=self.date_end
            ) | Q( # Valida si el inicio del nuevo horario se superpone con un horario existente desde adentro: Existente |   |
                date_init__lt=self.date_init,                                                                 # Nuevo      |    |
                date_end__gt=self.date_init
            ) | Q( # Valida si el final del nuevo horario se superpone con un horario existente desde adentro: Existente      |   |
                date_init__lt=self.date_end,                                                                 # Nuevo       |     |
                date_end__gt=self.date_end
            ),
            professional=self.professional
        ).exists()
        if overlapping_schedules:
            raise ValidationError("El horario que estas intentando crear se esta sobreponiendo con otro horario")
        return overlapping_schedules
