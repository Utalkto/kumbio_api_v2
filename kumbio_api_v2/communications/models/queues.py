"""Queues messages model."""

# Django
from django.db import models

# Models
from kumbio_api_v2.utils.models import KumbioModel
from kumbio_api_v2.users.models import User
from kumbio_api_v2.communications.models import MailTemplate


class QueueMessage(KumbioModel):
    class Type(models.TextChoices):
        WELCOME = "WELCOME", "Welcome Message"
        REMINDER = "REMINDER", "Reminder message"
        OTHER = "OTHER", "Other"

    user = models.ForeignKey(
        "users.user", on_delete=models.CASCADE, related_name="queue_messages", null=True, blank=True
    )
    phone_number = models.CharField(validators=[User.phone_regex], max_length=17, blank=True, null=True)
    attempts = models.PositiveIntegerField(default=0)
    delivery_date = models.DateTimeField(null=True, blank=True)
    date_sent = models.DateTimeField("Date sent", null=True, blank=True)
    sent = models.BooleanField(
        'was sent?',
        default=False,
        help_text='Set true when message is send.'
    )
    issue_sent = models.BooleanField(default=False)
    message_type = models.CharField(
        max_length=55,
        choices=Type.choices,
        default=Type.OTHER,
    )
    extra = models.JSONField(blank=True, null=True)
    template = models.ForeignKey(
        "communications.MailTemplate", on_delete=models.SET_NULL, blank=True, null=True, related_name="queues"
    )

    def __str__(self):
        return "Message of :{} to {}".format(self.message_type, self.user)
