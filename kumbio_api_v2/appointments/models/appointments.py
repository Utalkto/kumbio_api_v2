# Create your models here.

# Django
from django.db import models
from django.db.models import Q

# Rest Framework
from rest_framework.serializers import ValidationError

# Custom
from kumbio_api_v2.utils.models import KumbioModel, weekdays


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
        unique_together = (
            ("professional_user", "date", "hour_init"),
            ("professional_user", "date", "hour_end"),
            ("client_user", "date", "hour_init"),
            ("client_user", "date", "hour_end"),
        )

    def save(self, *args, **kwargs):
        self.check_duration()
        self.check_professional_user_availability()
        appointment = super().save(*args, **kwargs)
        return appointment

    def check_duration(self):
        minutes_end = (self.hour_end.hour / 60) + self.hour_end.minute
        minutes_init = (self.hour_init.hour / 60) + self.hour_init.minute
        if minutes_end - minutes_init > self.service.duration:
            raise ValidationError("La duración de la cita no coincide con la duración del servicio")
        return None

    def check_professional_user_availability(self):
        self.check_sede_schedule()
        self.check_professional_user_schedule()
        self.check_professional_user_appointments_overlapping()
        self.check_client_user_appointments_overlapping()
        return None

    def check_professional_user_appointments_overlapping(self):
        unavailable = Appointment.objects.filter(
            Q(
                Q(  # Valida si el nuevo horario se superpone con un horario existente desde afuera o es exactamente el mismo
                    hour_init__gt=self.hour_init, hour_end__lt=self.hour_end
                )
                | Q(  # Valida si el inicio del nuevo horario se superpone con un horario existente desde adentro
                    hour_init__lt=self.hour_init, hour_end__gt=self.hour_init
                )
                | Q(  # Valida si el final del nuevo horario se superpone con un horario existente desde adentro
                    hour_init__lt=self.hour_end, hour_end__gt=self.hour_end
                )
            )
            & ~Q(pk=self.pk),
            professional_user=self.professional_user,
            date=self.date,
        ).exists()
        if unavailable:
            raise ValidationError("La cita que intenta agendar se esta sobreponiendo con otra")
        return unavailable

    def check_client_user_appointments_overlapping(self):
        unavailable = Appointment.objects.filter(
            Q(
                Q(  # Valida si el nuevo horario se superpone con un horario existente desde afuera o es exactamente el mismo
                    hour_init__gt=self.hour_init, hour_end__lt=self.hour_end
                )
                | Q(  # Valida si el inicio del nuevo horario se superpone con un horario existente desde adentro
                    hour_init__lt=self.hour_init, hour_end__gt=self.hour_init
                )
                | Q(  # Valida si el final del nuevo horario se superpone con un horario existente desde adentro
                    hour_init__lt=self.hour_end, hour_end__gt=self.hour_end
                )
            )
            & ~Q(pk=self.pk),
            client_user=self.client_user,
            date=self.date,
        ).exists()
        if unavailable:
            raise ValidationError("El cliente ya tiene una cita en este horario")
        return unavailable

    def check_professional_user_schedule(self):
        available = (
            self.professional_user.professional.professional_schedule.all()
            .filter(
                day=weekdays[self.date.weekday()],
                hour_init__lte=self.hour_init,
                hour_end__gte=self.hour_end,
                is_working=True,
            )
            .exists()
            and not self.professional_user.professional.rest_professional_schedule.all()
            .filter(date_init__lte=self.date, date_end__gte=self.date)
            .exists()
        )
        if not available:
            raise ValidationError("Debido al horario del profesional no esta disponibile para esta cita")
        return available

    def check_sede_schedule(self):
        available = (
            self.sede.sede_schedule.all()
            .filter(
                day=weekdays[self.date.weekday()],
                hour_init__lte=self.hour_init,
                hour_end__gte=self.hour_end,
                is_working=True,
            )
            .exists()
        )
        if not available:
            raise ValidationError("Debido al horario de la sede el profesional no esta disponibile para esta cita")
        return available
