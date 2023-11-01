"""Organizations models"""

# Django
# Utils
from datetime import datetime, timedelta

from django.db import models

# Models
from kumbio_api_v2.utils.models import KumbioModel


class Organization(KumbioModel):
    """Organization model."""

    name = models.CharField(max_length=255)

    sub_sector = models.ForeignKey("SubSector", on_delete=models.CASCADE, related_name="organization_sectors", null=True, blank=True)

    description = models.TextField()

    country = models.ForeignKey("Country", on_delete=models.CASCADE, related_name="organization_country")

    currency = models.CharField("Moneda",max_length=120, default=None, null=True, blank=True)

    how_we_met = models.CharField("Como nos conocio", max_length=255, null=True, blank=True)

    class Meta:
        """Meta class."""

        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        return f"Organization {self.name} - {self.sub_sector}"


class OrganizationMembership(KumbioModel):
    """Organization membership model."""

    membership = models.ForeignKey("MembershipType", on_delete=models.CASCADE, related_name="organization_membership")

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="organization_membership")

    is_active = models.BooleanField(
        "Esta activa", default=False, help_text="Set to true when the user have an active membership."
    )
    start_date = models.DateField("Inicio de membresía", null=True, blank=True)
    expiration = models.DateField("Expiración de membresía", auto_now=False, auto_now_add=False)

    def save(self, *args, **kwargs):
        if not self.start_date or not self.expiration:
            days_durration = self.membership.trial_days
            date_now = datetime.now().date()
            date_expiration = date_now + timedelta(days=days_durration)
            self.start_date = date_now
            self.expiration = date_expiration
        super().save(*args, **kwargs)

    class Meta:
        """Meta class."""

        verbose_name = "Organization membreship"
        verbose_name_plural = "Organizations memberships"

    def __str__(self):
        return f"{self.organization.name}"
