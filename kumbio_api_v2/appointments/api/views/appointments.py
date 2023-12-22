"""appointments views."""

# Django REST Framework
# Utils
import logging
from datetime import datetime, timedelta

from django.db.models import Exists, OuterRef

# Django
from django.shortcuts import get_object_or_404
from rest_framework import mixins, response, status, views, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ValidationError

# Serializers
from kumbio_api_v2.appointments.api.serializers.appointments import AppointmentSerializer

# Models
from kumbio_api_v2.appointments.models import Appointment, DurationSchedule
from kumbio_api_v2.organizations.models import Professional, Sede, Service
from kumbio_api_v2.utils.models import weekdays


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
            self.professional_obj = get_object_or_404(Professional, pk=self.professional_pk)
            if hasattr(self, "date"):
                durations = self.get_duration_schedule()
                res.data = {"date": self.date.strftime("%Y-%m-%d"), "hours": durations}
                res.status_code = status.HTTP_200_OK
            else:
                self.date = self.now_date
                durations = self.get_professional_availability()
                res.data = {"date": self.date.strftime("%Y-%m-%d"), "hours": durations}
                res.status_code = status.HTTP_200_OK
        return res

    def get_date(self):
        self.now = datetime.now()
        self.now_date = self.now.date()
        self.now_time = self.now.time()
        if "date" in self.query_params:
            try:
                self.date = datetime.strptime(self.query_params["date"], "%Y-%m-%d").date()
            except Exception as e:
                logging.error(f"Error al convertir la fecha: {e}")
                raise ValidationError(f"Error al convertir la fecha: {e}")
            self.date = self.date if self.date >= self.now_date else self.now_date
        return None

    def get_professional_availability(self):
        allowed_days = self.get_allowd_days()
        if not allowed_days:
            raise ValidationError("El profesional no dispone de ningun calendario para trabajar")
        print(self.date)
        self.date += timedelta(days=-1)
        while True:
            self.date += timedelta(days=1)
            self.weekday = weekdays[self.date.weekday()]
            if self.weekday not in allowed_days:
                continue
            durations = self.get_duration_schedule()
            print(durations.exists())
            if durations.exists():
                return durations

    def get_duration_schedule(self):
        durations = (
            DurationSchedule.objects.filter(
                service=self.service_obj, professional_schedule__professional=self.professional_obj, day=self.weekday
            )
            .exclude(
                Exists(
                    Appointment.objects.filter(
                        professional_user=self.professional_obj.user,
                        date=self.date,
                        hour_init__gte=OuterRef("hour_init"),
                        hour_init__lt=OuterRef("hour_end"),
                    )
                ),
                Exists(
                    Appointment.objects.filter(
                        professional_user=self.professional_obj.user,
                        date=self.date,
                        hour_end__gt=OuterRef("hour_init"),
                        hour_end__lte=OuterRef("hour_end"),
                    )
                ),
                Exists(
                    Appointment.objects.filter(
                        professional_user=self.professional_obj.user,
                        date=self.date,
                        hour_init__lte=OuterRef("hour_init"),
                        hour_end__gte=OuterRef("hour_end"),
                    )
                ),
            )
            .values("hour_init", "hour_end")
        )
        if self.date == self.now_date and durations.exists():
            print(self.now_time)
            durations = durations.filter(hour_init__gte=self.now_time)
        return durations

    def get_allowd_days(self):
        allowed_days = list(
            DurationSchedule.objects.filter(
                service=self.service_obj, professional_schedule__professional=self.professional_obj
            ).values_list("day", flat=True)
        )
        return allowed_days
