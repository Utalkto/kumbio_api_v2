"""Professionals views."""

# from datetime import datetime

# # Django
# from django.db.models import Q, Subquery

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from kumbio_api_v2.organizations.api.serializers import ServiceProfessionalSerializer

# Models
from kumbio_api_v2.organizations.models import Professional, Sede, Service

# Serializers
from kumbio_api_v2.users.api.serializers import (
    ProfessionalModelSerializer,
    ProfessionalScheduleSerializer,
    ProfessionalSerializer,
    RestProfessionalScheduleModelSerializer,
)

# Utilities
from kumbio_api_v2.utils.utilities import professiona_availability


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
        "professional_schedule",
        "rest_professional_schedule",
    )

    def dispatch(self, request, *args, **kwargs):
        """Verify that the user exists."""
        self.tutorial = request.GET.get("tutorial")
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action in ["schedule_onboarding"]:
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

    @action(detail=False, methods=["POST"], url_path="schedule-onboarding")
    def schedule_onboarding(self, request, *args, **kwargs):
        """Add professional schedule."""
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request, "tutorial": self.tutorial},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["PUT", "PATCH"], url_path="schedule-update")
    def schedule_update(self, request, *args, **kwargs):
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
            data=request.data,
            context={"professional": instance},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="availability")
    def availability(self, request, *args, **kwargs):
        """Retrieve professional availability."""
        data = request.query_params
        professional_pk = int(data.get("professional_pk")) if data.get("professional_pk") != "all" else "all"
        service_pk = int(data.get("service_pk")) if data.get("service_pk") else None
        place_pk = int(data.get("place_pk")) if data.get("place_pk") else None
        date = data.get("date") if data.get("date") else None
        professional = (
            Professional.objects.select_related(
                "sede",
            )
            .prefetch_related(
                "professional_schedule",
                "rest_professional_schedule",
                "professional_appointments",
            )
            .get(pk=professional_pk)
            if professional_pk != "all"
            else "all"
        )
        service = Service.objects.get(pk=service_pk) if service_pk else None
        place = Sede.objects.get(pk=place_pk) if place_pk else None
        if not service or not professional or not place:
            raise ValidationError("la pk del profesional o el servicio o la sede no existen")
        else:
            professional_availability = professiona_availability(professional, place, service, date)
        data = professional_availability
        return Response(data, status=status.HTTP_200_OK)


class ProfesionalScheduleViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    lookup_field = "pk"
    permission_classes = [IsAuthenticated]
    serializer_class = ProfessionalScheduleSerializer
