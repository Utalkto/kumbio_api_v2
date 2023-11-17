"""Users serializers."""

# Django
import jwt
from django.conf import settings
from django.contrib.auth import authenticate

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

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
    phone_number = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255, required=False)
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        if isinstance(obj, User):
            return obj.get_full_name()
        elif isinstance(obj, dict):
            return obj.get("first_name", "") + " " + obj.get("last_name", "")
        else:
            return None

    def validate_phone_number(self, phone_number):
        """Check if phone number is unique."""
        if User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError("Ya existe un usuario registrado con ese número de teléfono.")
        return phone_number

    def validate_email(self, email):
        """Check if phone number is unique."""
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Ya existe un usuario registrado con este email.")
        return email

    class Meta:
        """Meta class."""

        model = User
        fields = (
            "first_name",
            "last_name",
            "full_name",
            "email",
            "phone_number",
        )


class UserSignUpSerializer(serializers.Serializer):
    """User sign up serializer.

    Handle sign up data validation.
    """

    first_name = serializers.CharField(min_length=2, max_length=255)
    last_name = serializers.CharField(min_length=2, max_length=255)
    phone_number = serializers.CharField(max_length=255)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8, max_length=64)

    def validate_phone_number(self, phone_number):
        """Check if phone number is unique."""
        if User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError("Ya existe un usuario registrado con ese número de teléfono.")
        return phone_number

    def validate_email(self, email):
        """Check if phone number is unique."""
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Ya existe un usuario registrado con este email.")
        return email

    def create(self, data):
        """Handle user and profile creation."""
        # Create user
        full_name = data.get("first_name") + " " + data.get("last_name")
        username = full_name.lower().replace(" ", "-")
        user = User.objects.create_user(username=username, is_owner=True, is_professional=True, **data)
        token = generate_auth_token(user)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email = payload.get("user")
        if isinstance(email, Token):
            token = email
            return token.key, token.user
        token = user.get_autorized_token
        return user, token


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
