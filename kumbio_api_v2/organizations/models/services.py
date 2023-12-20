from datetime import timedelta

from django.db import models

from kumbio_api_v2.appointments.models import DurationSchedule
from kumbio_api_v2.organizations.models import Professional, ProfessionalSchedule
from kumbio_api_v2.utils.models import KumbioModel


class Service(KumbioModel):
    """Service model."""

    name = models.CharField(max_length=255)
    duration = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    sedes = models.ManyToManyField("organizations.Sede", related_name="sede_services")
    description = models.TextField(blank=True, null=True)
    terms_and_conditions = models.TextField(blank=True, null=True)

    class Meta:
        """Meta class."""

        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __ini__(self, *args, **kwargs):
        self = super().__init__(*args, **kwargs)

        self.duration_current = self.duration

    def __str__(self):
        return f"Service {self.name}"

    def save(self, *args, **kwargs):
        durations = DurationSchedule.objects.only("pk").filter(service=self)

        if self.duration_current != self.duration:
            if durations.exists():
                durations.delete()
            self.create_duration_schedules()

        obj = super().save(*args, **kwargs)

        if not durations.exists():
            self.create_duration_schedules()
        return obj

    def create_duration_schedules(self, durationschedule):
        self.get_professional_schedules()
        if self.professional_schedules.exists() and self.duration > 0:
            for professional_schedule in self.professional_schedules.iterator():
                hour_init = professional_schedule.hour_init
                hour_end = professional_schedule.hour_end
                current_hour_end = hour_init + timedelta(minutes=self.duration)
                while True:
                    if current_hour_end >= hour_end:
                        break
                    DurationSchedule.objects.create(
                        professional_schedule=professional_schedule,
                        service=self,
                        hour_init=hour_init,
                        hour_end=current_hour_end,
                        day=professional_schedule.day,
                    )
                    hour_init = current_hour_end
                    current_hour_end += timedelta(minutes=self.duration)

    def get_professional_schedules(self):
        if not hasattr(self, "professional_schedules"):
            professional_ids = list(
                Professional.objects.filter(services=self).prefetch_related("professional_schedule").values_list("pk", flat=True)
            )

            self.professional_schedules = ProfessionalSchedule.objects.only("pk", "hour_init", "hour_end", "day").filter(
                professional_id__in=professional_ids, is_working=True
            )

        return None
