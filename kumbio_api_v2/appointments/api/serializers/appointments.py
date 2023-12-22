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


# class AppointmentSerializer(serializers.Serializer):

#     professional_id = serializers.IntegerField()
#     service_id = serializers.IntegerField()
#     place_id = serializers.IntegerField()
#     date = serializers.DateField(required=False)

#     def validate_professional_id(self, data):


#     # Validate professional, and services and places


# class AvailabilityAppointments(serializers.Serializer):

#     appointment = AppointmentSerializer(many=True)
