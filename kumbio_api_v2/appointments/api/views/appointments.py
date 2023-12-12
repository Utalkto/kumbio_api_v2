"""appointments views."""

# Django REST Framework
# Utils
from datetime import datetime

# Django
from django.shortcuts import get_object_or_404
from rest_framework import mixins, response, status, views, viewsets
from rest_framework.permissions import IsAuthenticated

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
    permission_classes = [IsAuthenticated]
    queryset = Appointment.objects.all().select_related("professional", "sede", "service")
    serializer_class = AppointmentSerializer


class ProfessionalAvailability(views.APIView):
    """
    Se utiliza un ApiView ya que la respuesta no es directa de un modelo
    sino que debe ser un rango de horas para agendar la cita en un dia especifico.
    """

    lookup_field = "pk"
    permission_classes = [IsAuthenticated]

    def get(self, request):
        self.query_params = request.query_params.dict()

        try:
            pk_sede = self.query_params["pk_sede"]
            pk_professional = self.query_params["pk_professional"]
            pk_service = self.query_params["pk_service"]
            self.date = datetime.strptime(self.query_params["date"], "%Y-%m-%d").date()
        except KeyError as e:
            return response.Response({"detail": f"Parameter {e} is required"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return response.Response({"detail": f"Parameter {e} is not valid"}, status=status.HTTP_400_BAD_REQUEST)

        self.sede_obj = get_object_or_404(Sede, pk=pk_sede)
        self.professional_obj = get_object_or_404(Professional, pk=pk_professional)
        self.service_obj = get_object_or_404(Service, pk=pk_service)

        return self.professional_availability()

    def professional_availability(self):
        pass
