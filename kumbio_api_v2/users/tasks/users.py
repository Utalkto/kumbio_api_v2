import email
from curses.ascii import US
from re import template

# templates
from kumbio_api_v2.communications.models.templates import MailTemplate

# communications
from kumbio_api_v2.communications.notification import replace_message_tags, send_email, send_whatsapp
from django.contrib.auth import get_user_model
from users.models import User

from config import celery_app
from kumbio_api_v2.conftest import user

User = get_user_model()


@celery_app.task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


@celery_app.task()
def owner_wellcome(owner: User):
    email = owner.email
    template = MailTemplate.objects.get(pk=0)  # TODO: change to email template
    data = {  # TODO: change to owner data
        "organization_owner_name": owner.name,
    }
    replace_message_tags(template.message, data)
    send_email(email, template.subject, template.message)


@celery_app.task()
def owner_wellcome_whatsapp(owner: User):
    # only if onboarding is complete
    # only if 1 headquarter is added
    # only if at least 1 service is added
    phone = owner.phone_number
    template = MailTemplate.objects.get(pk=0)  # TODO: change to whatsapp template
    data = {
        "organization_owner_name": owner.name,
        "organization_name": owner.organization.name,
        "organization_phone": owner.organization.phone_number,
    }
    replace_message_tags(template.message, data)
    send_whatsapp(phone, template.message)


@celery_app.task()
def owner_wellcome_whatsapp_not_complete_onboarding(owner: User):
    # only if onboarding is not complete
    # only if 1 headquarter is not added
    # only if at least 1 service is not added
    phone = owner.phone_number
    template = MailTemplate.objects.get(pk=0)  # TODO: change to whatsapp template
    data = {
        "organization_owner_name": owner.name,
        "organization_name": owner.organization.name,
        "organization_phone": owner.organization.phone_number,
    }
    replace_message_tags(template.message, data)
    send_whatsapp(phone, template.message)


@celery_app.task()
def schedule_first_appointment(owner: User):
    # 2 days after register
    # only if no appointment has been scheduled
    email = owner.email
    template = MailTemplate.objects.get(pk=0)  # TODO: change to email template
    data = {
        "organization_owner_name": owner.name,
    }
    replace_message_tags(template.message, data)
    send_email(email, template.subject, template.message)


@celery_app.task()
def add_all_your_services(owner: User):
    # 4 days after register
    # only if less than 3 services has been added
    email = owner.email
    template = MailTemplate.objects.get(pk=0)  # TODO: change to email template
    data = {
        "organization_owner_name": owner.name,
    }
    replace_message_tags(template.message, data)
    send_email(email, template.subject, template.message)


@celery_app.task()
def schedule_this_week_appointments(owner: User):
    # 6 days after register
    # only if less than 10 appointments has been scheduled from calendar
    email = owner.email
    template = MailTemplate.objects.get(pk=0)  # TODO: change to email template
    data = {
        "organization_owner_name": owner.name,
    }
    replace_message_tags(template.message, data)
    send_email(email, template.subject, template.message)


@celery_app.task()
def webpage_online_schedule(owner: User):
    # 8 days after register
    # only if less than 10 appointments has been scheduled from webpage
    email = owner.email
    template = MailTemplate.objects.get(pk=0)  # TODO: change to email template
    data = {
        "organization_owner_name": owner.name,
    }
    replace_message_tags(template.message, data)
    send_email(email, template.subject, template.message)


@celery_app.task()
def share_your_link(owner: User):
    # 10 days after register
    # only if less than 10 appointments has been scheduled from webpage
    email = owner.email
    template = MailTemplate.objects.get(pk=0)  # TODO: change to email template
    data = {
        "organization_owner_name": owner.name,
        "organization_name": owner.organization.name,
    }
    replace_message_tags(template.message, data)
    send_email(email, template.subject, template.message)


@celery_app.task
def premium_subscription_expiring(owner: User):
    # 14 days after register
    email = owner.email
    template = MailTemplate.objects.get(pk=0)  # TODO: change to email template
    data = {  # TODO: change to owner data
        "organization_owner_name": owner.name,
    }
    replace_message_tags(template.message, data)
    send_email(email, template.subject, template.message)


@celery_app.task
def how_you_doing(owner: User):
    # 17 days after register
    phone = owner.phone_number
    template = MailTemplate.objects.get(pk=0)  # TODO: change to whatsapp template
    data = {  # TODO: change to owner data
        "organization_owner_name": owner.name,
    }
    replace_message_tags(template.message, data)
    send_whatsapp(phone, template.message)


@celery_app.task
def professional_wellcome(professional: User):
    email = professional.email
    template = MailTemplate.objects.get(pk=0)  # TODO: change to email template
    data = {  # TODO: change to professional data
        "professional_name": professional.name,
    }
    message = replace_message_tags(template.message, data)
    send_email(email, template.subject, message)


@celery_app.task
def max_professionals_limit_reached(owner: User):
    email = owner.email
    template = MailTemplate.objects.get(pk=0)  # TODO: change to email template
    data = {  # TODO: change to owner data
        "organization_owner_name": owner.name,
        "professional_name": owner.name,
    }
    message = replace_message_tags(template.message, data)
    send_email(email, template.subject, message)


@celery_app.task
def max_appointments_reached(owner: User):
    email = owner.email
    template = MailTemplate.objects.get(pk=0)  # TODO: change to email template
    data = {  # TODO: change to owner data
        "organization_owner_name": owner.name,
        "professional_name": owner.name,
    }
    message = replace_message_tags(template.message, data)
    send_email(email, template.subject, message)


# TODO: todos los whatsapps son solo para el plan premium
