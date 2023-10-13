from django.db import models

from kumbio_api_v2.utils.models import KumbioModel

class Service(KumbioModel):
    """Service model."""

    name = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    sedes = models.ManyToManyField("organizations.Sede", related_name="sede_services")
    description = models.TextField(blank=True, null=True)
    

    class Meta:
        """Meta class."""

        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return f"Service {self.name}"
