"""Organizations models"""

# Django
from django.db import models

# Models
from kumbio_api_v2.utils.models import KumbioModel


class Organization(KumbioModel):
    """Organization model."""

    name = models.CharField(max_length=255)

    sub_sector = models.ForeignKey(
        "SubSector", on_delete=models.CASCADE, related_name="organization_sectors", null=True, blank=True
    )

    description = models.TextField()

    country = models.ForeignKey("Country", on_delete=models.CASCADE, related_name="organization_country")

    currency = models.CharField("Moneda", max_length=120, default=None, null=True, blank=True)

    how_you_know_us = models.CharField("Como nos conocio", max_length=120, default=None, null=True, blank=True)

    @property
    def professionals(self):
        from organizations.models.professionals import Professional

        return Professional.objects.filter(sede__organization=self)

    @property
    def all_organization_services(self):
        from kumbio_api_v2.organizations.models import Service

        return Service.objects.filter(sedes__organization=self).distinct()

    @property
    def headquarter(self):
        from kumbio_api_v2.organizations.models import Sede

        return Sede.objects.filter(organization=self).distinct()

    class Meta:
        """Meta class."""

        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        return f"Organization {self.name} - Sector {self.sub_sector}"


class OrganizationMembership(KumbioModel):
    """Organization membership model."""

    membership = models.ForeignKey("MembershipType", on_delete=models.CASCADE, related_name="organization_membership")

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="organization_membership")

    is_active = models.BooleanField(
        "Esta activa", default=False, help_text="Set to true when the user have an active membership."
    )
    start_date = models.DateField("Inicio de membresía", null=True, blank=True)
    expiration = models.DateField("Expiración de membresía", auto_now=False, auto_now_add=False)
    days_duration = models.IntegerField(default=30)
    email_notification = models.BooleanField(
        "Notificaciones por email",
        default=False,
        help_text="Cuando esta en True significa que puede enviar notificaciones vía email.",
    )
    whatsapp_notification = models.BooleanField(
        "Notificaciones por wpp",
        default=False,
        help_text="Cuando esta en True significa que puede enviar notificaciones vía wpp.",
    )
    email_notification_available = models.PositiveIntegerField(
        "Total notificaciones vía email disponibles.", default=0
    )
    wpp_notification_available = models.PositiveIntegerField("Total notificaciones vía wpp disponibles.", default=0)

    class Meta:
        """Meta class."""

        verbose_name = "Organization membreship"
        verbose_name_plural = "Organizations memberships"

    def __str__(self):
        return f"{self.organization.name}"
