# Django
from django.contrib import admin

# Models
from kumbio_api_v2.appointments.models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """Organization model admin."""

    list_display = ["professional", "sede", "service", "start_date", "hour_init", "hour_end"]
    search_fields = ["professional", "sede", "service"]
    date_hierarchy = "start_date"
