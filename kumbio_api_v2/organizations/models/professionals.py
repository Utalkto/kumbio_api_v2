from django.db import models

from kumbio_api_v2.utils.models import KumbioModel

class professional(KumbioModel):
    """Professional model."""

    #professional is not necessarily a user
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255, null=True, blank=True)
    organization = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="organization_professionals")
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
        return f"Professional {self.name} - {self.organization}"