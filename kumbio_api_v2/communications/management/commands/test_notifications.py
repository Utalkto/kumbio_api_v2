# Django
from django.core.management.base import BaseCommand

from kumbio_api_v2.communications.notification import send_email, send_whatsapp


class Command(BaseCommand):
    def handle(self, *args, **options):
        if send_whatsapp("+584124781318", "Hello, World! prueba realizada correctamente") is True:
            pass
        if not send_whatsapp("+584123058807", "Hello, World! prueba realizada correctamente"):
            pass
        if not send_whatsapp("+573126212123", "Hello, World! prueba realizada correctamente"):
            pass
        if not send_whatsapp("+14034012088", "Hello, World! prueba realizada correctamente"):
            pass

        if send_email("emiliojgerdezd@gmail.com", "Test Subject", "<p>Test Body</p>") is True:
            pass
        if not send_email("emiliojgerdezd@gmail.com", "Test Subject", "<p>Test Body</p>"):
            pass
