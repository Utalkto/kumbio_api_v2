"""Clients views."""

# Django REST Framework
from rest_framework import mixins, viewsets

# Permissions
from rest_framework.permissions import IsAuthenticated

# Serializers
from kumbio_api_v2.users.api.serializers.clients import ClientModelSerializer

# Models
from kumbio_api_v2.users.models import User


class ClientViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Clients view set."""

    queryset = User.objects.all()
    serializer_class = ClientModelSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"
