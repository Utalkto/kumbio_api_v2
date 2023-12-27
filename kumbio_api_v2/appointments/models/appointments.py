# Create your models here.

# Django
from django.db import models

# Custom
from kumbio_api_v2.utils.models import KumbioModel


class Appointment(KumbioModel):
    """Appointment model."""

    class PaymentStatusOptions(models.TextChoices):
        """Payment status options."""

        PAID = "PAID", "Pagado"
        PENDING = "PENDING", "Pendiente"
        CANCELED = "CANCELED", "Cancelado"

    class PaymentMethodOptions(models.TextChoices):
        """Payment method options."""

        CASH = "CASH", "Efectivo"
        TRANSFER = "TRANSFER", "Transferencia"
        STRIPE = "STRIPE", "Stripe"
        OTHER = "OTHER", "Otro"

    # only one service and professional per appointment for easier management
    # so we have to create a new appointment for each service
    # dont need organization because we have sede
    professional_user = models.ForeignKey(
        "users.User",
        limit_choices_to={"is_professional": True},
        on_delete=models.SET_NULL,
        related_name="professional_appointments",
        null=True,
    )
    sede = models.ForeignKey("organizations.Sede", on_delete=models.SET_NULL, related_name="sede_appointments", null=True)
    service = models.ForeignKey("organizations.Service", on_delete=models.SET_NULL, related_name="service_appointments", null=True)
    payment_status = models.CharField(max_length=10, choices=PaymentStatusOptions.choices, default=PaymentStatusOptions.PENDING)
    payment_method = models.CharField(max_length=10, choices=PaymentMethodOptions.choices, default=PaymentMethodOptions.CASH)
    date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    hour_init = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    hour_end = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    created_by_user = models.ForeignKey("users.User", on_delete=models.SET_NULL, related_name="created_appointments", null=True)
    client_user = models.ForeignKey(
        "users.User",
        limit_choices_to={"is_client": True},
        on_delete=models.SET_NULL,
        related_name="client_appointments",
        null=True,
    )

    class Meta:
        """Meta class."""

        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
