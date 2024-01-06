"""Appointmets professional serializers."""

# Utilities
# Django REST Framework
from rest_framework import serializers

# Models
from kumbio_api_v2.appointments.models.appointments import Appointment
from kumbio_api_v2.organizations.models import Professional, Sede, Service
from kumbio_api_v2.users.models import User


class AppointmentAvailability(serializers.Serializer):
    sede = serializers.PrimaryKeyRelatedField(queryset=Sede.objects.all())
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    professional_user = serializers.PrimaryKeyRelatedField(queryset=Professional.objects.all())
    client_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_client=True))
    date = serializers.DateField()
    hour_init = serializers.TimeField()
    hour_end = serializers.TimeField()
    payment_method = serializers.ChoiceField(
        choices=Appointment.PaymentMethodOptions.choices, default=Appointment.PaymentMethodOptions.CASH
    )

    def validate(self, data):
        validated_data = super().validate(data)

        sede = validated_data["sede"]
        service = validated_data["service"]
        professional_user = validated_data["professional_user"]

        if not sede:
            raise serializers.ValidationError("La sede no existe.")
        if not service:
            raise serializers.ValidationError("Este servicio no existe.")
        if not professional_user:
            raise serializers.ValidationError("Este professional no existe.")
        return validated_data

    def create(self, validated_data):
        request = self.context.get("request")
        created_by_user = request.user

        appointment = Appointment.objects.create(created_by_user=created_by_user, **validated_data)

        return appointment
