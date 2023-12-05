"""Queues messages model."""

# Django
from django.db import models

from kumbio_api_v2.users.models import User

# Models
from kumbio_api_v2.utils.models import KumbioModel


class QueueMessage(KumbioModel):
    class Type(models.TextChoices):
        WELCOME = "WELCOME", "Welcome Message"
        REMINDER = "REMINDER", "Reminder message"
        OTHER = "OTHER", "Other"

    id_message = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(
        "users.user", on_delete=models.CASCADE, related_name="queue_messages", null=True, blank=True
    )
    phone_number = models.CharField(validators=[User.phone_regex], max_length=17, blank=True, null=True)
    attempts = models.PositiveIntegerField(default=0)
    date_sent = models.DateTimeField("Date sent", null=True, blank=True)
    sent = models.BooleanField("was sent?", default=False, help_text="Set true when message is send.")
    issue_sent = models.BooleanField(default=False)
    message_type = models.CharField(
        max_length=55,
        choices=Type.choices,
        default=Type.OTHER,
    )
    notification_official = models.TextField(null=True, blank=True)
    extra = models.JSONField(blank=True, null=True)
    template = models.ForeignKey(
        "communications.MailTemplate", on_delete=models.SET_NULL, blank=True, null=True, related_name="queues"
    )

    def __str__(self):
        return f"Message of :{self.message_type} to {self.user}"
