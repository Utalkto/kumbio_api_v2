# Django
from django.db import models
from django.db.models import Q

# Custom
from kumbio_api_v2.utils.models import DaysChoices, KumbioModel

# Rest Framework
from rest_framework.exceptions import ValidationError


class Professional(KumbioModel):
    """Professional model."""

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="professional")
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

    def __str__(self):
        return f"Schedule {self.professional} - {self.day}"

    def save(self, *args, **kwargs):
        self.check_schedules_overlapping()
        schedule = super().save(*args, **kwargs)
        return schedule

    def check_schedules_overlapping(self):
        overlapping_schedules = ProfessionalSchedule.objects.filter(
            Q(
                hour_init__gte=self.hour_init,
                hour_end__lte=self.hour_end
            ) | Q(
                hour_init__lte=self.hour_init,
                hour_end__gte=self.hour_end
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

    def __str__(self):
        return f"Rest Professional Schedule {self.professional}"

    def save(self, *args, **kwargs):
        self.check_schedules_overlapping()
        schedule = super().save(*args, **kwargs)
        return schedule

    def check_schedules_overlapping(self):
        overlapping_schedules = RestProfessionalSchedule.objects.filter(
            Q(
                date_init__gte=self.date_init,
                date_end__lte=self.date_end
            ) | Q(
                date_init__lte=self.date_init,
                date_end__gte=self.date_end
            ),
            professional=self.professional
        ).exists()
        if overlapping_schedules:
            raise ValidationError("El horario que estas intentando crear se esta sobreponiendo con otro horario")
        return overlapping_schedules
