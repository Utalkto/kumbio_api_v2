from datetime import timezone

from celery.schedules import crontab

from config import celery_app
from kumbio_api_v2.appointments.models import Appointment

# Templates
from kumbio_api_v2.communications.models.templates import MailTemplate

# Communications
from kumbio_api_v2.communications.notification import replace_message_tags, send_email, send_whatsapp
from kumbio_api_v2.organizations.models import Organization, Service
from kumbio_api_v2.users.models import User


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=8, minute=00),
        check_user_status,
        name="check_user_status",
    )


@celery_app.task()
def check_user_status():
    usuarios = User.objects.all()
    for usuario in usuarios:
        if usuario.is_owner:
            # TODO refactor this
            if usuario.onboarding_complete and usuario.headquarters.count() == 1 and usuario.services.count() >= 1:
                owner_wellcome_whatsapp(usuario)
            else:
                owner_wellcome_whatsapp_not_complete_onboarding(usuario)
        register_date = usuario.date_joined
        days_since_register = (timezone.now() - register_date).days
        organization = Organization.objects.get(owner=usuario)
        appointments = Appointment.objects.filter(organization=organization).count()
        services = Service.objects.filter(organization=organization).count()
        if days_since_register >= 2 and appointments == 0:
            schedule_first_appointment(usuario)

        if days_since_register >= 4 and services < 3:
            add_all_your_services(usuario)

        if days_since_register >= 6 and appointments < 10:
            # TODO: check if appointments are from calendar or webpage
            schedule_this_week_appointments(usuario)
        if days_since_register >= 8 and appointments < 10:
            # TODO: check if appointments are from calendar or webpage
            webpage_online_schedule(usuario)
        if days_since_register >= 10 and appointments < 10:
            # TODO: check if appointments are from calendar or webpage
            share_your_link(usuario)
        if days_since_register >= 14:
            premium_subscription_expiring(usuario)
        if days_since_register >= 17:
            how_you_doing(usuario)


@celery_app.task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


@celery_app.task()
def owner_wellcome(owner: User):
    email = owner.email
    organization = Organization.objects.get(owner=owner)
    template = MailTemplate.objects.get(pk=1)  # TODO: change to email template
    data = {  # TODO: change to owner data
        "organization_owner_name": owner.name,
        "service_name": "example",
        "professional_name": "example",
        "place_name": "example",
        "place_address": "example",
        "organization_name": organization.name,
        "organization_phone": "example",  # organization.phone_number,
    }
    replace_message_tags(template.message, data)
    send_email(email, template.subject, template.message)


@celery_app.task()
def owner_wellcome_whatsapp(owner: User):
    # only if onboarding is complete
    # only if 1 headquarter is added
    # only if at least 1 service is added
    phone = owner.phone_number
    organization = Organization.objects.get(owner=owner)
    template = MailTemplate.objects.get(pk=2)  # TODO: change to whatsapp template
    data = {
        "organization_owner_name": owner.name,
        "service_name": "example",
        "professional_name": "example",
        "place_name": "example",
        "place_address": "example",
        "organization_name": organization.name,
        "organization_phone": "example",  # organization.phone_number,
    }
    replace_message_tags(template.message, data)
    send_whatsapp(phone, template.message)


@celery_app.task()
def owner_wellcome_whatsapp_not_complete_onboarding(owner: User):
    # only if onboarding is not complete
    # only if 1 headquarter is not added
    # only if at least 1 service is not added
    phone = owner.phone_number
    organization = Organization.objects.get(owner=owner)
    template = MailTemplate.objects.get(pk=3)  # TODO: change to whatsapp template
    data = {
        "organization_owner_name": owner.name,
        "service_name": "example",
        "professional_name": "example",
        "place_name": "example",
        "place_address": "example",
        "organization_name": organization.name,
        "organization_phone": "example",  # organization.phone_number,
    }
    replace_message_tags(template.message, data)
    send_whatsapp(phone, template.message)


@celery_app.task()
def schedule_first_appointment(owner: User):
    # 2 days after register
    # only if no appointment has been scheduled
    email = owner.email
    template = MailTemplate.objects.get(pk=4)  # TODO: change to email template
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
    template = MailTemplate.objects.get(pk=5)  # TODO: change to email template
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
    template = MailTemplate.objects.get(pk=6)  # TODO: change to email template
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
    template = MailTemplate.objects.get(pk=7)  # TODO: change to email template
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
    organization = Organization.objects.get(owner=owner)
    template = MailTemplate.objects.get(pk=8)  # TODO: change to email template
    data = {
        "organization_owner_name": owner.name,
        "organization_name": organization.name,
    }
    replace_message_tags(template.message, data)
    send_email(email, template.subject, template.message)


@celery_app.task
def premium_subscription_expiring(owner: User):
    # 14 days after register
    email = owner.email
    template = MailTemplate.objects.get(pk=11)  # TODO: change to email template
    data = {  # TODO: change to owner data
        "organization_owner_name": owner.name,
    }
    replace_message_tags(template.message, data)
    send_email(email, template.subject, template.message)


@celery_app.task
def how_you_doing(owner: User):
    # 17 days after register
    phone = owner.phone_number
    template = MailTemplate.objects.get(pk=12)  # TODO: change to whatsapp template
    data = {  # TODO: change to owner data
        "client_name": owner.name,
    }
    replace_message_tags(template.message, data)
    send_whatsapp(phone, template.message)


@celery_app.task
def professional_wellcome(professional: User, owner: User):
    email = professional.email
    template = MailTemplate.objects.get(pk=19)  # TODO: change to email template
    data = {  # TODO: change to professional data
        "professional_name": professional.name,
        "organization_owner_name": owner.name,
        "organization_name": Organization.objects.get(owner=owner).name,
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
