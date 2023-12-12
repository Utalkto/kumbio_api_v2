"""Sedes views."""

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Serializers
from kumbio_api_v2.organizations.api.serializers.sedes import OrganizationSedeModelSerializer, SedeProfessionalModelSerializer

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
    lookup_field = "pk"
    permission_classes = [IsAuthenticated]
    queryset = Sede.objects.all().prefetch_related("sede_schedule", "sede_services", "organization_professionals__user")

    def get_serializer_class(self):
        if self.action in ["professionals"]:
            return SedeProfessionalModelSerializer
        else:
            return OrganizationSedeModelSerializer

    # @action(detail=True, methods=["GET"], url_path=r"professionals")
    # def professionals(self, request, *args, **kwargs):
    #     sede = self.get_object()
    #     if sede:
    #         organization = sede.organization
    #         professionals = organization.professionals.all()
    #         serializer = self.get_serializer(professionals, many=True)
    #         data = serializer.data
    #     return Response(data, status=status.HTTP_200_OK)
