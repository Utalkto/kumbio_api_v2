"""Organizations models"""

# Django
from django.db import models

# Models
from kumbio_api_v2.utils.models import KumbioModel


class Organization(KumbioModel):
    """Organization model."""

    name = models.CharField(max_length=255)

    sector = models.ForeignKey("Sector", on_delete=models.CASCADE, related_name="organization_sectors")

    description = models.TextField()

    country = models.CharField(max_length=120, default=None, null=True, blank=True)

    currency = models.CharField(max_length=120, default=None, null=True, blank=True)

    class Meta:
        """Meta class."""

        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        return f"Organization {self.name} - {self.sector}"


class OrganizationMembership(KumbioModel):
    """Organization membership model."""

    membership = models.ForeignKey("MembershipType", on_delete=models.CASCADE, related_name="organization_membership")

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="organization_membership")

    is_active = models.BooleanField(
        "Active", default=False, help_text="Set to true when the user have an active membership."
    )
    start_date = models.DateField("Iinit date", null=True, blank=True)
    expiration = models.DateField("Expiration date", auto_now=False, auto_now_add=False)

    class Meta:
        """Meta class."""

        verbose_name = "Organization membreship"
        verbose_name_plural = "Organizations memberships"

    def __str__(self):
        return f"{self.organization.name}"
