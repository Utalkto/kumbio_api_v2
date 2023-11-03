"""Appointmets professional serializers."""


# Django REST Framework
from rest_framework import serializers

# Models
from kumbio_api_v2.organizations.models import HeadquarterSchedule, Professional, ProfessionalSchedule, Sede, Service
from kumbio_api_v2.users.models import User