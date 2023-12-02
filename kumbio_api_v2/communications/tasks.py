"""Tasks communications."""

# Celery
from config import celery_app
from celery.schedules import crontab

# Apis
from kumbio_api_v2.utils.apis.ultra_message import UltraMessage


@celery_app.task(name="send_message_whatsapp")
def send_message_whatsapp(user, template):
    ultra_msg = UltraMessage()
    message = 
    obj_metric = None
    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        user = None
        logger.error(f"User with pk {user_pk} does not exists.")
    if user:
        metric = MeideiApi()
        obj_metric = metric.send_metric(user_pk=user.pk, action=action, data=extra_data)
    return obj_metric
