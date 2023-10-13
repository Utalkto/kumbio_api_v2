from django.db import models

from kumbio_api_v2.utils.models import KumbioModel

class Professional(KumbioModel):
    """Professional model."""

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="professional")
    sede = models.ForeignKey("organizations.Sede", on_delete=models.CASCADE, related_name="organization_professionals")
    services = models.ManyToManyField("organizations.Service", related_name="service_professionals")
    is_user = models.BooleanField(default=False)
    #need to add a field for the professional's schedule during the week
    #maybe a json field with the days and hours available
    #or a table with the days and hours available
    #json field is easier to implement
    #table is easier to query


    class Meta:
        """Meta class."""

        verbose_name = "Professional"
        verbose_name_plural = "Professionals"

    def __str__(self):
        return f"Professional {self.user.email} - {self.sede.name}"