"""Professionals views."""

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from kumbio_api_v2.organizations.api.serializers import ServiceProfessionalSerializer

# Models
from kumbio_api_v2.organizations.models import Professional, Sede

# Serializers
from kumbio_api_v2.users.api.serializers import ProfessionalScheduleSerializer, ProfessionalSerializer, ProfessionalScheduleAvailableSerializer


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
    queryset = Professional.objects.all().prefetch_related('professional_schedule')

    def dispatch(self, request, *args, **kwargs):
        """Verify that the user exists."""
        self.professional_pk = kwargs.get("pk")
        self.tutorial = request.GET.get("tutorial")
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action in ["schedule"]:
            return ProfessionalScheduleSerializer
        if self.action in ["service"]:
            return ServiceProfessionalSerializer
        if self.action in ["available_schedule"]:
            return ProfessionalScheduleAvailableSerializer
        else:
            return ProfessionalSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action not in ["schedule"]:
            context.update({"tutorial": self.tutorial})
        return context

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        fist_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        phone_number = request.data.get("phone_number")
        email = request.data.get("email")
        description = request.data.get("description")
        sede_pk = request.data.get("sede_pk")
        # Update user data
        user = instance.user
        user.first_name = fist_name
        user.last_name = last_name
        user.email = email
        user.phone_number = phone_number
        user.save()
        # Update professional data
        instance.description = description
        if sede_pk:
            instance.sede = Sede.objects.get(id=sede_pk)
        instance.save()
        data = {"result": "OK"}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], url_path="schedule")
    def schedule(self, request, *args, **kwargs):
        """Add professional schedule."""
        serializer = self.get_serializer(
            data=request.data,
            context={"professional": self.professional_pk, "tutorial": self.tutorial},
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
    
    @action(detail=True, methods=["GET"], url_path="available-schedule")
    def available_schedule(self, request, *args, **kwargs):
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
