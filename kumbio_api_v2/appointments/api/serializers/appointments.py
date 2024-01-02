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


# class AppointmentAvailability(serializers.Serializer):

#     service_pk = serializers.IntegerField()
#     place_pk = serializers.IntegerField()
#     date = serializers.DateField(required=False)

#     def get_service_pk(self, data):
#         try:
#             service = Service.objects.get(pk=data)
#         except Service.DoesNotExist:
#             raise serializers.ValidationError("Este servicio no existe.")
#         return service

#     def get_place_pk(self, data):
#         try:
#             place = Sede.objects.get(pk=data)
#         except Sede.DoesNotExist:
#             raise serializers.ValidationError("Esta sede no existe.")
#         return place


# class AvailabilityAppointments(serializers.Serializer):

#     appointment = ProfessionalAvailability(many=True)