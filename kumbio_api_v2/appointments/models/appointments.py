# Create your models here.

# Django
from django.db import models
from django.db.models import Q

# Custom
from kumbio_api_v2.utils.models import KumbioModel

# Rest Framework
from rest_framework.exceptions import ValidationError


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
        "users.User", limit_choices_to={"is_professional": True}, on_delete=models.SET_NULL, related_name="professional_appointments", null=True
    )
    sede = models.ForeignKey("organizations.Sede", on_delete=models.SET_NULL, related_name="sede_appointments", null=True)
    service = models.ForeignKey("organizations.Service", on_delete=models.SET_NULL, related_name="service_appointments", null=True)
    payment_status = models.CharField(
        max_length=10, choices=PaymentStatusOptions.choices, default=PaymentStatusOptions.PENDING
    )
    payment_method = models.CharField(
        max_length=10, choices=PaymentMethodOptions.choices, default=PaymentMethodOptions.CASH
    )
    date = models.DateField(auto_now=False, auto_now_add=False)
    hour_init = models.TimeField(auto_now=False, auto_now_add=False)
    hour_end = models.TimeField(auto_now=False, auto_now_add=False)
    created_by_user = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, related_name="created_appointments", null=True
    )
    client_user = models.ForeignKey(
        "users.User", limit_choices_to={"is_client": True}, on_delete=models.SET_NULL, related_name="client_appointments", null=True
    )

    class Meta:
        """Meta class."""

        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"

    def save(self, *args, **kwargs):
        self.check_professional_user_availability()
        appointment = super().save(*args, **kwargs)
        return appointment

    def check_professional_user_availability(self):
        self.check_professional_user_appointments_overlapping()
        self.check_client_user_appointments_overlapping()
        self.check_professional_user_schedule()
        self.check_sede_schedule()
        return None

    def check_professional_user_appointments_overlapping(self):
        unavailable = Appointment.objects.filter(
            professional_user=self.professional_user,
            date=self.date,
            hour_init__gt=self.hour_init,
            hour_end__lt=self.hour_end,
        ).exists()
        if unavailable:
            raise ValidationError("La cita que intenta agendar se esta sobreponiendo con otra")
        return unavailable

    def check_client_user_appointments_overlapping(self):
        unavailable = Appointment.objects.filter(
            client_user=self.client_user,
            date=self.date,
            hour_init__gt=self.hour_init,
            hour_end__lt=self.hour_end,
        ).exists()
        if unavailable:
            raise ValidationError("El cliente ya tiene una cita en este horario")
        return unavailable

    def check_professional_user_schedule(self):
        available = self.professional_user.professional_schedules.filter(
            day=self.date,
            hour_init__lte=self.hour_init,
            hour_end__gte=self.hour_end,
        ).exists()
        if not available:
            raise ValidationError("Debido al horario del usuario el profesional no esta dispobile para esta cita")
        return available

    def check_sede_schedule(self):
        available = self.sede.sede_schedules.filter(
            day=self.date,
            hour_init__lte=self.hour_init,
            hour_end__gte=self.hour_end,
        ).exists()
        if not available:
            raise ValidationError("Debido al horario de la sede el profesional no esta dispobile para esta cita")
        return available
