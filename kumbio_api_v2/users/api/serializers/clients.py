"""Clients serializers."""

# Django REST Framework
from rest_framework import serializers

# Serializers
from kumbio_api_v2.users.api.serializers.users import UserModelSerializer

# Models
from kumbio_api_v2.users.models import Profile, User


class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer."""

    class Meta:
        """Meta class."""

        model = Profile
        fields = "__all__"


class ClientModelSerializer(serializers.ModelSerializer):
    """Profile model serializer."""

    user_data = UserModelSerializer()
    profile_data = ProfileModelSerializer(read_only=True)
    organization_pk = serializers.IntegerField()

    class Meta:
        """Meta class."""

        model = User
        fields = ["user_data", "profile_data", "organization_pk"]

    def create(self, data):
        """Create and return a new `Profile` instance, given the validated data."""
        user_data = data.get("user_data")
        organization_pk = data.get("organization_pk")
        user = User.objects.create_user(**user_data, is_client=True)
        if user:
            # Create profile
            Profile.objects.create(user=user, organization_id=organization_pk, is_main=True)
            data["user_data"]["pk"] = user.pk
        return data
