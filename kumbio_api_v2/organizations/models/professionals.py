# Django
# Utils
from datetime import timedelta

from django.db import models
from django.db.models import Q

# Rest Framework
from rest_framework.serializers import ValidationError

from kumbio_api_v2.appointments.models import DurationSchedule

# Custom
from kumbio_api_v2.utils.models import DaysChoices, KumbioModel


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_hour_init = self.self.hour_init
        self.current_hour_end = self.self.hour_end

    def __str__(self):
        return f"Schedule {self.professional} - {self.day}"

    def save(self, *args, **kwargs):
        self.check_schedules_overlapping()

        durations = DurationSchedule.objects.only("pk").filter(professional_schedule=self)

        if self.hour_init != self.current_hour_init or self.hour_end != self.current_hour_end:
            if durations.exists():
                durations.delete()
            self.create_duration_schedules()

        obj = super().save(*args, **kwargs)

        if not durations.exists():
            self.create_duration_schedules(DurationSchedule)
        return obj

    def check_schedules_overlapping(self):
        overlapping_schedules = ProfessionalSchedule.objects.filter(
            Q(
                Q(  # Valida si el nuevo horario se superpone con un horario existente desde afuera o es exactamente el mismo
                    hour_init__gt=self.hour_init, hour_end__lt=self.hour_end
                )
                | Q(  # Valida si el inicio del nuevo horario se superpone con un horario existente desde adentro: Existente
                    hour_init__lt=self.hour_init, hour_end__gt=self.hour_init
                )
                | Q(  # Valida si el final del nuevo horario se superpone con un horario existente desde adentro
                    hour_init__lt=self.hour_end, hour_end__gt=self.hour_end
                )
            )
            & ~Q(pk=self.pk),
            professional=self.professional,
            day=self.day,
        )
        if overlapping_schedules.exists():
            raise ValidationError("El horario se sobrepone con otro horario")

    def create_duration_schedules(self):
        self.get_professional_services()
        for service in self.professional_services.iterator():
            hour_init = self.hour_init
            hour_end = self.hour_end
            current_hour_end = hour_init + timedelta(minutes=service.duration)
            if service.duration > 0:
                while True:
                    if current_hour_end >= hour_end:
                        break
                    DurationSchedule.objects.create(
                        professional_schedule=self,
                        service=service,
                        hour_init=hour_init,
                        hour_end=current_hour_end,
                        day=self.day,
                    )
                    hour_init = current_hour_end
                    current_hour_end += timedelta(minutes=self.duration)

    def get_professional_services(self):
        if not hasattr(self, "professional_services"):
            self.professional_services = self.professional.services.only("id", "duration").all()
        return None


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
            Q(
                Q(  # Valida si el nuevo horario se superpone con un horario existente desde afuera o es exactamente el mismo
                    date_init__gt=self.date_init, date_end__lt=self.date_end
                )
                | Q(  # Valida si el inicio del nuevo horario se superpone con un horario existente desde adentro
                    date_init__lt=self.date_init, date_end__gt=self.date_init
                )
                | Q(  # Valida si el final del nuevo horario se superpone con un horario existente desde adentro
                    date_init__lt=self.date_end, date_end__gt=self.date_end
                )
            )
            & ~Q(pk=self.pk),
            professional=self.professional,
        ).exists()
        if overlapping_schedules:
            raise ValidationError("El horario que estas intentando crear se esta sobreponiendo con otro horario")
        return overlapping_schedules
