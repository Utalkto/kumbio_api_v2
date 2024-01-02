"""appointments views."""


# Django
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

# Serializers
from kumbio_api_v2.appointments.api.serializers.appointments import AppointmentAvailability

# Models
from kumbio_api_v2.appointments.models import Appointment


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
    queryset = Appointment.objects.all().select_related("professional", "sede", "service")
    serializer_class = AppointmentAvailability
