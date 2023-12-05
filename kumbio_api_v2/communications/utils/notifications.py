"""Notifications utils."""

# Django
from kumbio_api_v2.users.models import User


def get_params_message(user, message, service=None, sede=None, **kwargs):
    """translate message variables and return the entire message."""

    if "{client_name}" in message:
        if isinstance(user, User):
            message = message.replace("{client_name}", user.get_full_name())
        else:
            message = message.replace("{client_name}", "")
    return message
