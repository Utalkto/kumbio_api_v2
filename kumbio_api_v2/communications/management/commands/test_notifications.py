from cgi import test
from unittest.mock import patch

from kumbio_api_v2.communications.notification import send_email, send_whatsapp

# Django
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_whatsapp("+584124781318", "Hello, World! prueba realizada correctamente") == True
        send_whatsapp("+584123058807", "Hello, World! prueba realizada correctamente") == False
        send_whatsapp("+573126212123", "Hello, World! prueba realizada correctamente") == False
        send_whatsapp("+14034012088", "Hello, World! prueba realizada correctamente") == False

        send_email("emiliojgerdezd@gmail.com", "Test Subject", "<p>Test Body</p>") == True
        send_email("emiliojgerdezd@gmail.com", "Test Subject", "<p>Test Body</p>") == False
