# Create your models here.

from django.db import models

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
    
    class CreatedByOptions(models.TextChoices):
        """Created by options."""

        CLIENT = "CLIENT", "Cliente"
        ADMIN = "ADMIN", "Administrador"

    #only one service and professional per appointment for easier management
    #so we have to create a new appointment for each service
    #dont need organization because we have sede
    payment_status = models.CharField( max_length=10, choices=PaymentStatusOptions.choices, default=PaymentStatusOptions.PENDING)
    payment_method = models.CharField( max_length=10, choices=PaymentMethodOptions.choices, default=PaymentMethodOptions.CASH)
    professional = models.ForeignKey("organizations.Professional", on_delete=models.CASCADE, related_name="professional_appointments")
    sede = models.ForeignKey("organizations.Sede", on_delete=models.CASCADE, related_name="sede_appointments")
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    created_by = models.CharField( max_length=10, choices=CreatedByOptions.choices, default=CreatedByOptions.CLIENT)
    service = models.ForeignKey("services.Service", on_delete=models.CASCADE, related_name="service_appointments")

    class Meta:
        """Meta class."""

        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"

    def __str__(self):
        return f"Appointment {self.name} - {self.description}"