"""Appointmets professional serializers."""

# Utilities
# Django REST Framework
from rest_framework import serializers

# Models
from kumbio_api_v2.appointments.models import Appointment
from kumbio_api_v2.organizations.models import Professional
from kumbio_api_v2.utils.models import weekdays


class AppointmentSerializer(serializers.ModelSerializer):
    """Appointment model serializer."""

    class Meta:
        model = Appointment
        fields = "__all__"


class ProfessionalAvailabilitySerializer(serializers.Serializer):
    """Professional availability serializer."""

    professional_pk = serializers.IntegerField(source="pk")
    user_pk = serializers.IntegerField(source="user.pk")
    availability = serializers.SerializerMethodField()
    appointments = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.date = kwargs["context"].get("date")
        super().__init__(*args, **kwargs)

    def get_availability(self, obj):
        return list(
            obj.professional_schedule.all().filter(day=weekdays[self.date.weekday()], is_working=True).values("hour_init", "hour_end")
        )

    def get_appointments(self, obj):
        return list(obj.user.professional_appointments.filter(date=self.date).values("client_user", "hour_init", "hour_end"))

    class Meta:
        model = Professional
