import email
from email import message
from tarfile import data_filter

from appointments.models import Appointment

# templates
from kumbio_api_v2.communications.models.templates import MailTemplate

# communications
from kumbio_api_v2.communications.notification import replace_message_tags, send_email, send_whatsapp

from config import celery_app


@celery_app.task()
def appointment_confirm(appointment: Appointment):
    email = appointment.client.email
    template = MailTemplate.objects.get(pk=0)  # TODO: change to email template
    data = {  # TODO: change to client data
        "client_name": appointment.client.name,
        "professional_name": appointment.professional.name,
        "service_name": appointment.service.name,
        "sede_name": appointment.sede.name,
        "start_date": appointment.start_date,
        "end_date": appointment.end_date,
    }
    message = replace_message_tags(template.message, data)
    send_email(email, template.subject, message)
    phone = appointment.client.phone_number
    template = MailTemplate.objects.get(pk=0)  # TODO: change to whatsapp template
    data = {}
    data = {  # TODO: change to client data to whatsapp
        "client_name": appointment.client.name,
        "professional_name": appointment.professional.name,
        "service_name": appointment.service.name,
        "sede_name": appointment.sede.name,
        "start_date": appointment.start_date,
        "end_date": appointment.end_date,
    }
    messsage = replace_message_tags(template.message, data)
    send_whatsapp(phone, messsage)


@celery_app.task()
def absence_rescheduling(appointment: Appointment):
    # only if plan is pro or premium
    # if client mark as absent
    email = appointment.client.email  # TODO: change to client email
    template = MailTemplate.objects.get(pk=0)
    data = {  # TODO: change to client data
        "client_name": appointment.client.name,
        "professional_name": appointment.professional.name,
        "service_name": appointment.service.name,
        "sede_name": appointment.sede.name,
        "start_date": appointment.start_date,
        "end_date": appointment.end_date,
    }
    message = replace_message_tags(template.message, data)
    send_email(email, template.subject, message)
    phone = appointment.client.phone_number
    template = MailTemplate.objects.get(pk=0)  # TODO: change to whatsapp template
    data = {}
    data = {  # TODO: change to client data to whatsapp
        "client_name": appointment.client.name,
        "professional_name": appointment.professional.name,
        "service_name": appointment.service.name,
        "sede_name": appointment.sede.name,
        "start_date": appointment.start_date,
        "end_date": appointment.end_date,
    }
    messsage = replace_message_tags(template.message, data)
    send_whatsapp(phone, messsage)


@celery_app.task()
def thanks_receipt(appointment: Appointment):
    # only if free plan
    email = appointment.client.email
    template = MailTemplate.objects.get(pk=0)  # TODO: change to email template
    data = {  # TODO: change to client data
        "client_name": appointment.client.name,
        "professional_name": appointment.professional.name,
        "service_name": appointment.service.name,
        "sede_name": appointment.sede.name,
        "start_date": appointment.start_date,
        "end_date": appointment.end_date,
    }
    message = replace_message_tags(template.message, data)
    send_email(email, template.subject, message)


@celery_app.task()
def thanks_receipt_survey(appointment: Appointment):
    # only if pro or premium plan
    email = appointment.client.email
    template = MailTemplate.objects.get(pk=0)  # TODO: change to email template
    data = {  # TODO: change to client data
        "client_name": appointment.client.name,
        "professional_name": appointment.professional.name,
        "service_name": appointment.service.name,
        "sede_name": appointment.sede.name,
        "start_date": appointment.start_date,
        "end_date": appointment.end_date,
    }
    message = replace_message_tags(template.message, data)
    send_email(email, template.subject, message)
