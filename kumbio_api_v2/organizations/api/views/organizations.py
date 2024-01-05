"""Organization views."""
# Django
from django.db.models import Prefetch

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# Serializers
from kumbio_api_v2.organizations.api.serializers import (
    OrganizationModelSerializer,
    OrganizationProfessionalModelSerializer,
    OrganizationSedeModelSerializer,
    SectorModelSerializer,
)
from kumbio_api_v2.organizations.api.serializers.services import ServicesOrganizationModelSerializer

# Models
from kumbio_api_v2.organizations.models import Organization, Professional, Sector, Sede, Service
from kumbio_api_v2.users.api.serializers.users import UserModelSerializer
from kumbio_api_v2.users.models import User


class OrganizationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Organization view set."""

    queryset = Organization.objects.all().prefetch_related("organization_sedes")
    lookup_field = "pk"
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["services"]:
            return ServicesOrganizationModelSerializer
        if self.action in ["sedes"]:
            return OrganizationSedeModelSerializer
        if self.action in ["clients"]:
            return UserModelSerializer
        else:
            return OrganizationModelSerializer

    @action(detail=True, methods=["GET"], url_path=r"services")
    def services(self, request, *args, **kwargs):
        organization = self.get_object()
        services = (
            Service.objects.filter(sedes__organization=organization)
            .distinct()
            .prefetch_related(Prefetch("sedes", queryset=Sede.objects.filter(organization=organization)))
        )
        serializer = self.get_serializer(services, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"], url_path=r"sedes")
    def sedes(self, request, *args, **kwargs):
        organization = self.get_object()
        sedes = Sede.objects.filter(organization=organization).select_related("organization").prefetch_related("sede_schedule")
        serializer = self.get_serializer(sedes, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"], url_path=r"clients")
    def clients(self, request, *args, **kwargs):
        organization = self.get_object()
        clients = User.objects.filter(profile__organization=organization).select_related("profile__organization")
        serializer = self.get_serializer(clients, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


class OrganizationProfessionalsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """List organization professionals."""

    serializer_class = OrganizationProfessionalModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        organization_pk = self.kwargs["organization_pk"]
        return Professional.objects.filter(sede__organization_id=organization_pk)


class SectorViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """List sectors and subsectors."""

    queryset = Sector.objects.all()
    serializer_class = SectorModelSerializer
    permission_classes = [AllowAny]
