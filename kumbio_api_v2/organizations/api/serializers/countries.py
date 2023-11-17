"""Country serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from kumbio_api_v2.organizations.models import Country


class CountryModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = [
            "id",
            "name",
            "slug_name",
            "phone_prefix",
        ]
