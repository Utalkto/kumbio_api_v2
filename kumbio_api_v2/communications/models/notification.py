from django.db import models
from kumbio_api_v2.utils.models import KumbioModel
from kumbio_api_v2.users.models import User
from kumbio_api_v2.organizations.models import Organization

from enum import Enum

class MessageType(Enum):
    NOTIFICATION = 1
    REMINDER = 2
    ADMINS = 3

class Notification(models.Model):
    Organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="organization_notifications")
    type = models.IntegerField(choices=[(tag, tag.value) for tag in MessageType])
    template = models.ForeignKey("Template", on_delete=models.CASCADE, related_name="template_notifications")
    sent = models.BooleanField(default=False)
    send_date = models.DateTimeField(null=True, blank=True)
    sent_date = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    data = models.JSONField(null=True, blank=True)
    appoinment = models.ForeignKey("appointments.Appointment", on_delete=models.CASCADE, related_name="appointment_notifications", null=True, blank=True)
    
    