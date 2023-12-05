# Django
from django.db import models

# Models
from kumbio_api_v2.utils.models import KumbioModel


class MessageChannel(models.IntegerChoices):
    EMAIL = 1
    SMS = 2
    WHATSAPP = 3


class MailTemplate(KumbioModel):
    """TYemplates notifications model."""

    name: str = models.CharField(max_length=120)
    slug_name = models.SlugField(unique=True, max_length=120)
    subject: str = models.CharField(max_length=255, blank=True, null=True)
    message: str = models.TextField()
    type: MessageChannel = models.IntegerField(choices=MessageChannel.choices, default=MessageChannel.EMAIL)

    class Meta:
        # Constraints
        constraints = [
            models.CheckConstraint(
                check=~models.Q(type=MessageChannel.EMAIL, subject=""), name="email_subject_not_empty"
            )
        ]

    def __str__(self):
        return f"{self.pk} - {self.name}"
