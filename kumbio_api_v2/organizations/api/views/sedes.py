"""Sedes views."""

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Serializers
from kumbio_api_v2.organizations.api.serializers import (
    OrganizationSedeSerializer,
    ProfessionalScheduleSerializer,
    ProfessionalSerializer,
    ServiceProfessionalSerializer,
)

# Models
from kumbio_api_v2.organizations.models import Sede


class SedeViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = OrganizationSedeSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        organization_pk = self.kwargs.get("organization_pk")
        queryset = Sede.objects.filter(organization__pk=organization_pk)
        return queryset


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

    def dispatch(self, request, *args, **kwargs):
        """Verify that the user exists."""
        self.professional_pk = kwargs.get("pk")
        self.sede_pk = kwargs.get("sede_pk")
        self.tutorial = request.GET.get("tutorial")
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action in ["schedule"]:
            return ProfessionalScheduleSerializer
        if self.action in ["service"]:
            return ServiceProfessionalSerializer
        else:
            return ProfessionalSerializer
        return super().get_serializer_class()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action not in ["schedule"]:
            context.update({"sede_pk": self.sede_pk, "tutorial": self.tutorial})
        return context

    @action(detail=True, methods=["POST"], url_path="schedule")
    def schedule(self, request, *args, **kwargs):
        """Add professional schedule."""

        serializer = self.get_serializer(
            data=request.data,
            context={"professional": self.professional_pk, "sede": self.sede_pk, "tutorial": self.tutorial},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {"created": "ok", "professional_pk": self.professional_pk, "sede_pk": self.sede_pk}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], url_path="service")
    def service(self, request, *args, **kwargs):
        """Add professional service."""
        serializer = self.get_serializer(
            data=request.data,
            context={"professional": self.professional_pk, "sede": self.sede_pk, "tutorial": self.tutorial},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {"created": "ok", "professional_pk": self.professional_pk, "sede_pk": self.sede_pk}
        return Response(data, status=status.HTTP_200_OK)
