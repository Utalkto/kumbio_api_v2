"""Professionals views."""

# from datetime import datetime

# # Django
# from django.db.models import Q, Subquery

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from kumbio_api_v2.organizations.api.serializers import ServiceProfessionalSerializer

# Models
from kumbio_api_v2.organizations.models import Professional, Sede

# Serializers
from kumbio_api_v2.users.api.serializers import (
    ProfessionalScheduleSerializer,
    ProfessionalSerializer,
    ProfessionalModelSerializer,
    RestProfessionalScheduleModelSerializer
)


class ProfesionalViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    lookup_field = "pk"
    permission_classes = [IsAuthenticated]
    queryset = Professional.objects.all().prefetch_related(
        "professional_schedule", "rest_professional_schedule", "professional_appointments")

    def dispatch(self, request, *args, **kwargs):
        """Verify that the user exists."""
        self.tutorial = request.GET.get("tutorial")
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action in ["schedule"]:
            return ProfessionalScheduleSerializer
        if self.action in ["rest_professional"]:
            return RestProfessionalScheduleModelSerializer
        if self.action in ["service"]:
            return ServiceProfessionalSerializer
        if self.action in ["retrieve"]:
            return ProfessionalModelSerializer
        else:
            return ProfessionalSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action not in ["schedule"]:
            context.update({"tutorial": self.tutorial})
        return context

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user_data = data.get("user_data")
        sede_pk = data.get("sede_pk")
        first_name = user_data.get("first_name")
        last_name = user_data.get("last_name")
        email = user_data.get("email")
        phone_number = user_data.get("phone_number")
        # Update user data
        user = instance.user
        user.first_name = first_name if first_name else user.first_name
        user.last_name = last_name if last_name else user.last_name
        user.email = email if email else user.email
        user.phone_number = phone_number if phone_number else user.phone_number
        user.save()
        # Update professional data
        instance.description = data.get("description")
        if sede_pk:
            instance.sede = Sede.objects.get(id=sede_pk)
        instance.save()
        data = {"result": "OK"}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], url_path="schedule")
    def schedule(self, request, *args, **kwargs):
        """Add professional schedule."""
        instance = self.get_object()
        serializer = self.get_serializer(
            data=request.data,
            context={"professional": instance, "tutorial": self.tutorial},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], url_path="service")
    def service(self, request, *args, **kwargs):
        """Add professional service."""
        instance = self.get_object()
        serializer = self.get_serializer(
            data=request.data,
            context={"professional": instance},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], url_path="rest-professional")
    def rest_professional(self, request, *args, **kwargs):
        """Add professional service."""
        instance = self.get_object()
        request.data["professional"] = instance.pk
        serializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    # @action(detail=True, methods=["GET"], url_path="available-schedule")
    # def available_schedule(self, request, *args, **kwargs):
    #     """Add professional service."""
    #     instance = self.get_object()
    #     date = request.GET.get("date")
    #     date = datetime.strptime(date, "%Y-%m-%d")
    #     day_of_week = date.strftime('%A').upper()
    #     professional_schedule = instance.professional_schedule.filter(day=day_of_week).values_list("hour_init")
    #     professional_appointments = instance.professional_appointments.filter(
    #       start_date__date=date).values_list("start_date__time")
    #     professional_rest = instance.rest_professional_schedule.filter(
    #         day=day_of_week,
    #         hour_init__isnull=False,
    #         hour_end__isnull=False,
    #     ).values('hour_init', 'hour_end')
    #     time_available = professional_schedule.exclude(
    #         Q(hour_init__in=Subquery(professional_appointments.values('start_date__time'))) |
    #         Q(hour_end__in=Subquery(professional_appointments.values('start_date__time'))) |
    #         Q(hour_init__in=Subquery(professional_rest.values('hour_init'))) |
    #         Q(hour_end__in=Subquery(professional_rest.values('hour_end'))
    #     ))
    #     return Response("ok", status=status.HTTP_200_OK)
