"""Users serializers."""

# Django
# from django.conf import settings
# from django.contrib.auth import password_validation, authenticate
# from django.core.validators import RegexValidator

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Models
from kumbio_api_v2.users.models import User
from kumbio_api_v2.organizations.models import (
    Organization,
    OrganizationMembership,
    MembershipType,
    Sede
)


# Utilities


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    first_name = serializers.CharField(
        min_length=2,
    )
    last_name = serializers.CharField(
        min_length=2,
    )

    class Meta:
        """Meta class."""

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
        )


class UserSignUpSerializer(serializers.Serializer):
    """User sign up serializer.

    Handle sign up data validation.
    """

    organization_name = serializers.CharField(
        max_length=255
    )
    sector = serializers.IntegerField()
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8, max_length=64)

    def create(self, data):
        """Handle user and profile creation."""
        organization_name = data.get("organization_name")
        sector = data.get("sector")
        email = data.get("email")
        password = data.get("password")
        # Create organization
        organization = Organization.objects.create(name=organization_name, sector_id=sector)
        # Create membreship
        OrganizationMembership.objects.create(
            membership=MembershipType.objects.get(membership_type="PREMIUM"),
            organization=organization,
            is_active=True,
        )
        # Create sede
        Sede.objects.create(
            name=organization_name,
            organization=organization,
        )
        # Create user
        User.objects.create_user(email=email, password=password,  is_owner=True)
        data.pop("password")
        return data


class UserLoginSerializer(serializers.Serializer):
    """User login serializer.

    Handle the login request data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials."""
        user = User.objects.all()
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet :(')
        self.context['user'] = user
        return data

    def create(self, data):
        """Generate or retrieve new token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key
