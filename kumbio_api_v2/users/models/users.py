# Django
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Rest framework
from rest_framework.authtoken.models import Token

from kumbio_api_v2.users.managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for kumbio_api_v2.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    username = models.CharField(max_length=150, blank=True)
    phone_regex = RegexValidator(
        regex=r"\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(max_length=17, blank=True, null=True)
    is_client = models.BooleanField("Cliente", default=False, help_text=("Indica si el usuario es cliente"))
    is_owner = models.BooleanField("Owner", default=False, help_text=("Indica si el usuario es propietario"))
    is_administrator = models.BooleanField("Admin", default=False, help_text=("Indica si el usuario es administrador"))
    is_professional = models.BooleanField("Profesional", default=False, help_text=("Indica si el usuario es profesional"))
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

    @property
    def get_authorized_token(self):
        token, _is_new = Token.objects.update_or_create(user=self)
        return token.key
