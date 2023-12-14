from django.urls import path

from kumbio_api_v2.appointments.api.views import ProfessionalAvailability

app_name = "appointments"
urlpatterns = [
    path("professional-availability/", ProfessionalAvailability.as_view(), name="professional-availability"),
]
