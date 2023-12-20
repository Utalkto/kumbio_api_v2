"""Appointmets professional serializers."""

# Utilities
# Django REST Framework
from rest_framework import serializers

# Models
from kumbio_api_v2.appointments.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    """Appointment model serializer."""

    class Meta:
        model = Appointment
        fields = "__all__"
