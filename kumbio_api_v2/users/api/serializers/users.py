"""Users serializers."""

# Django
import jwt
from django.conf import settings
from django.contrib.auth import authenticate

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from kumbio_api_v2.organizations.models import Country, MembershipType, Organization, OrganizationMembership, Sede

# Models
from kumbio_api_v2.users.models import User

# Utilities
from kumbio_api_v2.utils.utilities import generate_auth_token


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
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
        )


class UserSignUpSerializer(serializers.Serializer):
    """User sign up serializer.

    Handle sign up data validation.
    """

    organization_name = serializers.CharField(max_length=255)
    sector = serializers.IntegerField()
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8, max_length=64)
    country = serializers.CharField(max_length=255)

    def create(self, data):
        """Handle user and profile creation."""
        organization_name = data.get("organization_name")
        sector = data.get("sector")
        email = data.get("email")
        password = data.get("password")
        country = data.get("country")
        country = Country.objects.filter(slug_name=country).first()
        # Create organization
        organization = Organization.objects.create(name=organization_name, sector_id=sector, country=country)
        # Create membreship
        OrganizationMembership.objects.create(
            membership=MembershipType.objects.get(membership_type="PREMIUM"),
            organization=organization,
            is_active=True,
        )
        # Create sede
        sede = Sede.objects.create(
            name=organization_name,
            organization=organization,
        )
        # Create user
        User.objects.create_user(email=email, password=password, is_owner=True)
        data.pop("password")
        data["sede_pk"] = sede.pk
        return data


class UserLoginSerializer(serializers.Serializer):
    """User login serializer.

    Handle the login request data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        self.context["user"] = user
        return data

    def create(self, data):
        """Generate or retrieve new token."""
        user = self.context.get("user")
        token = generate_auth_token(user)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email = payload.get("user")
        if isinstance(email, Token):
            token = email
            return token.key, token.user
        user = User.objects.filter(email=email).last()
        token = user.get_autorized_token
        return user, token
