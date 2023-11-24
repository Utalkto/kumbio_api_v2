"""Profile model."""

# Django
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

# Models
from kumbio_api_v2.utils.models import KumbioModel


class Profile(KumbioModel):
    """Profile holds a users content data preference.
    """

    class DocumentType(models.TextChoices):
        CEDULA = 'CEDULA', _('Cédula de ciudadanía')
        TI = 'TI', _('Tarjeta de identidad')
        DNI = 'DNI', _('Dni')
        CEDULA_EX = 'CEDULA_EX', _('Cédula de extranjería')
        PASS = 'PASS', _('Pasaporte')

    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='profile')
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='organization_profile'
    )
    photo = models.FileField(upload_to='users/photos', null=True, blank=True)
    document_type = models.CharField(
        max_length=255,
        choices=DocumentType.choices,
        default=DocumentType.CEDULA,
        blank=True, null=True
    )

    document_number = models.CharField(
        max_length=50,
        blank=True, null=True
    )

    gender_type = models.CharField(
        max_length=255,
        blank=True, null=True
    )
    extra_fields = models.JSONField(
        null=True,
        blank=True
    )
    birthdate = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)

    phone_regex = RegexValidator(
        regex=r"\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed.",
    )
    phone_number_2 = models.CharField(max_length=20, blank=True, null=True)
    emergency_contact = models.CharField(max_length=255, blank=True, null=True)
    observations = models.TextField(blank=True, null=True)
    is_main = models.BooleanField("Cliente principal", default=False, help_text=("Es el cliente principal"))
    is_secondary = models.BooleanField("Cliente dependiente", default=False, help_text=("Es el cliente dependiente"))

    def __str__(self):
        """Return users name."""
        return f"Profile for {self.user.email}"

    class Meta:
        """Meta class."""

        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuarios"
