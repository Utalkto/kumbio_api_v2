# Django
from django.db import models


class MembershipType(models.Model):
    """Membership model."""

    class MembershipTypeOptions(models.TextChoices):
        """User staff permissions dashboard."""

        FREE = "FREE", "Gratis"
        PRO = "PRO", "Pro"
        PREMIUM = "PREMIUM", "Premium"

    membership_type = models.CharField(
        max_length=10, choices=MembershipTypeOptions.choices, default=MembershipTypeOptions.FREE
    )

    appointments_allowed = models.PositiveIntegerField("Citas permitidas", null=True, blank=True)

    places_allowed = models.PositiveIntegerField("Sedes permitidas", null=True, blank=True)

    services_allowed = models.PositiveIntegerField("Servicios permitidos", null=True, blank=True)

    professionals_allowed = models.PositiveIntegerField("Profesionales permitidos", null=True, blank=True)

    email_notifications_allowed = models.PositiveIntegerField("Notificaciones permitidas", null=True, blank=True)

    email_reminders_allowed = models.PositiveIntegerField("Recordatorios permitidos", null=True, blank=True)

    price = models.FloatField("Pricio membresía", null=True, blank=True)

    trial_days = models.PositiveIntegerField(default=14)

    class Meta:
        verbose_name = "Membresía"
        verbose_name_plural = "Membresías"

    def __str__(self):
        return self.get_membership_type_display()
