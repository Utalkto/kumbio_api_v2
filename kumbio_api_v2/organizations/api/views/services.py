# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Models
from kumbio_api_v2.organizations.models import Sede


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
    queryset = Sede.objects.all()
