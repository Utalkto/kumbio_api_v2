"""Professionals serializers."""

# Django


# Django REST Framework
from rest_framework import serializers

# Serializers
from kumbio_api_v2.organizations.api.serializers.sedes import HeadquarterScheduleSerializer

# Models
from kumbio_api_v2.organizations.models import Professional, ProfessionalSchedule, Sede
from kumbio_api_v2.users.models import User


class ProfessionalScheduleModelSerializer(serializers.ModelSerializer):
    """Service model serializer."""

    class Meta:
        """Meta class."""

        model = ProfessionalSchedule
        fields = "__all__"


class ProfessionalSerializer(serializers.Serializer):
    """Professional model serializer."""

    first_name = serializers.CharField(min_length=2, max_length=255)
    last_name = serializers.CharField(min_length=2, max_length=255)
    phone_number = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255, required=False)
    sede_pk = serializers.IntegerField(required=False)

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

    def create(self, validated_data):
        request = self.context.get("request")
        tutorial = self.context.get("tutorial")
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        phone_number = validated_data.get("phone_number")
        email = validated_data.get("email")
        sede_pk = validated_data.get("sede_pk")
        # Create user
        if tutorial:
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.phone_number = phone_number
            user.is_professional = True
            user.save()
        else:
            user = User.objects.create_user(
                phone_number=phone_number,
                first_name=first_name,
                email=email,
                last_name=last_name,
                is_professional=True,
            )
        if sede_pk:
            sede = Sede.objects.get(id=sede_pk)
        Professional.objects.create(user=user, sede=sede, is_user=True)
        return validated_data


class ProfessionalScheduleSerializer(serializers.Serializer):
    """Proffesional schedule serializer."""

    professional_schedule = serializers.ListField(child=serializers.DictField(required=True))

    def create(self, validated_data):
        sede = self.context.get("sede")
        professional = self.context.get("professional")
        tutorial = self.context.get("tutorial")
        professional_schedule = validated_data.get("professional_schedule")
        for schedule in professional_schedule:
            schedule["professional"] = professional
            serializer_professional = ProfessionalScheduleModelSerializer(data=schedule)
            serializer_professional.is_valid(raise_exception=True)
            serializer_professional.save()
            if tutorial:
                schedule.pop("professional")
                schedule["sede"] = sede
                serializer_headquarter = HeadquarterScheduleSerializer(data=schedule)
                serializer_headquarter.is_valid(raise_exception=True)
                serializer_headquarter.save()
        professional
        return professional