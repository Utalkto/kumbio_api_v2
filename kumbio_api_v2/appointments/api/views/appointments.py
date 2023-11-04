"""appointments views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

# Serializers
from kumbio_api_v2.appointments.api.serializers.appointments import AppointmentSerializer

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
    permission_classes = [IsAuthenticated]
    queryset = Appointment.objects.all().prefetch_related("professional", "sede", "service")
    serializer_class = AppointmentSerializer
