# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

# Serializers
from kumbio_api_v2.organizations.api.serializers.services import ServicesOrganizationModelSerializer

# Models
from kumbio_api_v2.organizations.models import Service


class ServicesViewset(
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
    queryset = Service.objects.all()
    serializer_class = ServicesOrganizationModelSerializer
