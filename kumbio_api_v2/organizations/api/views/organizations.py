"""Organization views."""

# Django REST Framework
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated

# Serializers
from kumbio_api_v2.organizations.api.serializers import (
    OrganizationModelSerializer,
    OrganizationProfessionalModelSerializer,
    SectorModelSerializer,
    OrganizationSedeModelSerializer
)
from kumbio_api_v2.organizations.api.serializers.services import ServicesOrganizationModelSerializer

# Models
from kumbio_api_v2.organizations.models import Organization, Professional, Sector


class OrganizationViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """Organization view set.

    Handle sign up, login and account verification.
    """

    queryset = Organization.objects.all().prefetch_related("organization_sedes")
    lookup_field = "pk"
    serializer_class = OrganizationModelSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['services']:
            return ServicesOrganizationModelSerializer
        if self.action in ['sedes']:
            return OrganizationSedeModelSerializer
        else:
            return OrganizationModelSerializer

    @action(detail=True, methods=['GET'], url_path=r'services')
    def services(self, request, *args, **kwargs):
        organization = self.get_object()
        services = organization.all_organization_services
        serializer = self.get_serializer(services, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['GET'], url_path=r'sedes')
    def sedes(self, request, *args, **kwargs):
        organization = self.get_object()
        sedes = organization.headquarter
        serializer = self.get_serializer(sedes, many=True)
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
