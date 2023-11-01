"""Users views."""

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# Serializers
from kumbio_api_v2.users.api.serializers import UserLoginSerializer, UserModelSerializer, UserSignUpSerializer

# Models
from kumbio_api_v2.users.models import User


class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """User view set.

    Handle sign up, login and account verification.
    """

    queryset = User.objects.filter()
    lookup_field = "pk"

    def get_serializer_class(self):
        """Return serializer based on action."""
        action_mappings = {
            "login": UserLoginSerializer,
            "signup": UserSignUpSerializer,
            "partial": UserModelSerializer,
        }
        return action_mappings.get(self.action, UserModelSerializer)

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ["signup", "login"]:
            permissions = [AllowAny]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data = {"result": "OK"}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def login(self, request):
        """User sign in."""
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {"user": UserModelSerializer(user).data, "access_token": token}
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["POST"])
    def signup(self, request):
        """User sign up."""
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {"user": UserModelSerializer(user).data, "access_token": token}
        return Response(data, status=status.HTTP_201_CREATED)
