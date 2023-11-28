from django.db import models

from kumbio_api_v2.utils.models import KumbioModel


class MessageChannel(models.IntegerChoices):
    EMAIL = 1
    SMS = 2
    WHATSAPP = 3


class MailTemplate(KumbioModel):
    name: str = models.CharField(max_length=120)
    subject: str = models.CharField(max_length=255)
    message: str = models.TextField()
    type: MessageChannel = models.IntegerField(choices=MessageChannel.choices, default=MessageChannel.EMAIL)

    def __str__(self):
        return f"{self.pk} - {self.name}"
