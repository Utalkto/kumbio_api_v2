"""Clients serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from kumbio_api_v2.users.models import Profile, User

# Serializers
from kumbio_api_v2.users.api.serializers.users import UserModelSerializer


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

    class Meta:
        """Meta class."""

        model = User
        fields = "__all__"

    def create(self, validated_data):
        """Create and return a new `Profile` instance, given the validated data."""
        import ipdb; ipdb.set_trace()
        user_data = validated_data.pop("user_data")
        user = User.objects.create_user(**user_data, is_client=True)
        if user:
            # Create profile
            profile = Profile.objects.create(user=user)
            return profile
        return validated_data
