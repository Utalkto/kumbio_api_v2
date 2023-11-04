from enum import Enum

from django.db import models


class MessageChannel(Enum):
    EMAIL = 1
    SMS = 2
    WHATSAPP = 3


class MailTemplate(models.Model):
    name: str = models.CharField(max_length=120)
    subject: str = models.CharField(max_length=255)
    message: str = models.TextField()
    type: MessageChannel = models.IntegerField(choices=[(tag, tag.value) for tag in MessageChannel])

    def __str__(self):
        return f"{self.pk} - {self.name}"
