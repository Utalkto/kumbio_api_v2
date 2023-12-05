"""Tasks communications."""

# Celery
from config import celery_app

# Utils
from kumbio_api_v2.communications.utils.notifications import get_params_message

# Apis
from kumbio_api_v2.utils.apis.ultra_message import UltraMessage


@celery_app.task(name="send_message_whatsapp")
def send_message_whatsapp(user, template):
    ultra_msg = UltraMessage()
    message = template.message
    message_decode = get_params_message(user, message)
    phone_number = int(user.phone_number)
    response = ultra_msg.send_whatsapp_message(phone_number, message_decode)
    return response, message_decode
