"""appointments views."""


# Django
from rest_framework import mixins, response, status, views, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ValidationError

# Serializers
from kumbio_api_v2.appointments.api.serializers.appointments import AppointmentSerializer

# Models
from kumbio_api_v2.appointments.models import Appointment
from kumbio_api_v2.organizations.models import Professional, Sede, Service


class AppointmentProfesionalViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    lookup_field = "pk"
    permission_classes = [AllowAny]
    queryset = Appointment.objects.all().select_related("professional_user", "sede", "service")
    serializer_class = AppointmentSerializer
