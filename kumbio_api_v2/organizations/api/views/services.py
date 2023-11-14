# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Serializers
from kumbio_api_v2.organizations.api.serializers.services import ServicesOrganizationModelSerializer

# Models
from kumbio_api_v2.organizations.models import Service


class ServicesOrganizationViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Services organization view set."""

    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        organization_pk = self.kwargs.get("organization_pk")
        queryset = Service.objects.filter(sedes__organization_id=organization_pk).distinct()
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ServicesOrganizationModelSerializer(many=True)
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ServicesOrganizationModelSerializer(queryset, many=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
