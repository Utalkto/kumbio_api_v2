from enum import Enum

from django.db import models

from kumbio_api_v2.utils.models import KumbioModel


class MessageChannel(Enum):
    EMAIL = 1
    SMS = 2
    WHATSAPP = 3


class MailTemplate(KumbioModel):
    name: str = models.CharField(max_length=120)
    subject: str = models.CharField(max_length=255)
    message: str = models.TextField()
    type: MessageChannel = models.IntegerField(choices=[(tag, tag.value) for tag in MessageChannel])

    def __str__(self):
        return f"{self.pk} - {self.name}"
