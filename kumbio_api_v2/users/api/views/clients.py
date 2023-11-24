"""Clients views."""

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# Models
from kumbio_api_v2.users.models import User, Profile

# Serializers
from kumbio_api_v2.users.api.serializers.clients import (
    ClientModelSerializer
)


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
