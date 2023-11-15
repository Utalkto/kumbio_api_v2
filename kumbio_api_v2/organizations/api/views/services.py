# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

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
