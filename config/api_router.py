# Django
from django.conf import settings

# REST framework
from rest_framework.routers import DefaultRouter, SimpleRouter

from kumbio_api_v2.organizations.api import views as organization_views

# Views
from kumbio_api_v2.users.api import views as user_views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(r"users", user_views.UserViewSet, basename="users")
router.register(r"organizations", organization_views.OrganizationViewSet, basename="organizations")
router.register(r"organizations/(?P<organization_pk>[^/.]+)/sedes", organization_views.SedeViewset, basename="sedes")
router.register(
    r"sede/(?P<sede_pk>[^/.]+)/profesional", organization_views.ProfesionalViewset, basename="proffesionals"
)


app_name = "api"
urlpatterns = router.urls
