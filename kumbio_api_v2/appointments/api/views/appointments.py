"""appointments views."""

# Django REST Framework
# Utils
import logging
from datetime import datetime

# Django
from django.shortcuts import get_object_or_404
from rest_framework import mixins, response, status, views, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ValidationError

# Serializers
from kumbio_api_v2.appointments.api.serializers.appointments import AppointmentSerializer, ProfessionalAvailabilitySerializer

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


class ProfessionalAvailability(views.APIView):
    """
    Se utiliza un ApiView ya que la respuesta no es directa de un modelo
    sino que debe ser un rango de horas para agendar la cita en un dia especifico.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        self.query_params = request.query_params.dict()
        self.sede_pk = self.query_params.get("sede_pk")
        self.professional_pk = self.query_params.get("professional_pk")
        self.service_pk = self.query_params.get("service_pk")
        self.get_date()

        self.sede_obj = get_object_or_404(Sede, pk=self.sede_pk)
        self.service_obj = get_object_or_404(Service, pk=self.service_pk)

        return self.get_response()

    def get_response(self):
        res = response.Response()
        res.status_code = status.HTTP_404_NOT_FOUND
        if self.professional_pk:
            res.data = self.get_professional_availability()
            res.status_code = status.HTTP_200_OK
        elif self.sede_pk and self.service_pk and self.date:
            res.data = self.get_prefessionals_availability()
            res.status_code = status.HTTP_200_OK
        return res

    def get_professional_availability(self):
        self.professional_obj = get_object_or_404(Professional, pk=self.professional_pk)
        return ProfessionalAvailabilitySerializer(self.professional_obj, context={"date": self.date}).data

    def get_prefessionals_availability(self):
        self.professionals = Professional.objects.filter(sede=self.sede_obj, services=self.service_obj).prefetch_related(
            "professional_schedule", "user__professional_appointments"
        )
        return ProfessionalAvailabilitySerializer(self.professionals, many=True, context={"date": self.date}).data

    def get_date(self):
        try:
            self.date = datetime.strptime(self.query_params["date"], "%Y-%m-%d").date()
        except Exception as e:
            logging.error(f"Error al convertir la fecha: {e}")
            raise ValidationError(f"Error al convertir la fecha: {e}")
        return None
