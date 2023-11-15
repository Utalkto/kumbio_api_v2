from django.db import models

from kumbio_api_v2.utils.models import DaysChoices, KumbioModel


class Professional(KumbioModel):
    """Professional model."""

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="professional")
    description = models.TextField(max_length=255, blank=True, null=True)
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
    """Professional schedule."""

    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name="professional_schedule")
    day = models.CharField(max_length=10, choices=DaysChoices.choices, default=DaysChoices.MONDAY)
    hour_init = models.TimeField()
    hour_end = models.TimeField()
    hour_init_rest = models.TimeField(blank=True, null=True)
    hour_end_rest = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"Schedule {self.professional} - {self.day}"


class RestProfessionalSchedule(KumbioModel):
    """Rest professional schedule."""

    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name="rest_professional_schedule")
    date_init = models.DateField()
    date_end = models.DateField()
    description = models.TextField(max_length=255, blank=True, null=True)
