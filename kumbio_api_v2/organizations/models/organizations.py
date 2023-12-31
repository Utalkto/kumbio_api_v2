"""Organizations models"""

# Django
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# Models
from kumbio_api_v2.utils.models import KumbioModel


class Organization(KumbioModel):
    """Organization model."""

    class Language(models.TextChoices):
        SPANISH = "SPANISH", "Español"
        ENGLISH = "ENGLISH", "Inglés"

    name = models.CharField(max_length=255)

    email = models.EmailField(_("email address"), unique=True, blank=True, null=True)

    description = models.TextField(max_length=255, blank=True, null=True)

    sub_sector = models.ForeignKey("SubSector", on_delete=models.CASCADE, related_name="organization_sectors", null=True, blank=True)

    description = models.TextField()

    country = models.ForeignKey("Country", on_delete=models.CASCADE, related_name="organization_country")

    currency = models.CharField("Moneda", max_length=120, default=None, null=True, blank=True)

    web_site = models.CharField("Link sitio web", max_length=60, default=None, null=True, blank=True)
    phone_regex = RegexValidator(
        regex=r"\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(max_length=17, blank=True, null=True)
    how_you_know_us = models.CharField("Como nos conocio", max_length=60, default=None, null=True, blank=True)

    onboarding_state = models.CharField("Estado de onboarding", max_length=120, default="organization_created", null=True, blank=True)

    language = models.CharField(choices=Language.choices, default=Language.SPANISH)

    automatic_reminder = models.BooleanField(default=False)

    minimun_days_reserve = models.PositiveIntegerField(default=0)

    @property
    def sectors(self):
        from organizations.models.sectors import Sector

        return Sector.objects.filter(organization=self)

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

    is_active = models.BooleanField("Esta activa", default=False, help_text="Set to true when the user have an active membership.")
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
    email_notification_available = models.PositiveIntegerField("Total notificaciones vía email disponibles.", default=0)
    wpp_notification_available = models.PositiveIntegerField("Total notificaciones vía wpp disponibles.", default=0)

    class Meta:
        """Meta class."""

        verbose_name = "Organization membreship"
        verbose_name_plural = "Organizations memberships"

    def __str__(self):
        return f"{self.organization.name}"
