from django.db import models

from kumbio_api_v2.utils.models import DaysChoices, KumbioModel


class Professional(KumbioModel):
    """Professional model."""

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="professional")
    sede = models.ForeignKey("organizations.Sede", on_delete=models.CASCADE, related_name="organization_professionals")
    services = models.ManyToManyField("organizations.Service", related_name="service_professionals")
    is_user = models.BooleanField(default=False)

    @property
    def organization(self):
        return self.sede.organization

    class Meta:
        """Meta class."""

        verbose_name = "Professional"
        verbose_name_plural = "Professionals"

    def __str__(self):
        return f"Professional {self.user.email} - {self.sede.name}"


class ProfessionalSchedule(KumbioModel):
    """Headquarters schedule."""

    day = models.CharField(max_length=10, choices=DaysChoices.choices, default=DaysChoices.MONDAY)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name="professional_schedule")
    hour_init = models.TimeField()
    hour_end = models.TimeField()
