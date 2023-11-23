# Celery
import email
from curses.ascii import US
from email import message
from re import U

from celery.schedules import crontab

# templates
from communications.models.template import MailTemplate

# communications
from kumbio_api_v2.communications.notification import replace_message_tags, send_email, send_whatsapp
from users.models import User

from config import celery_app

# Models
from kumbio_api_v2.organizations.models import OrganizationMembership


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(day_of_week="*", hour=00, minute=00),
        check_organization_memberships,
        name="check_organization_memberships",
    )


@celery_app.task
def check_organization_memberships():
    """Check user memberships"""
    user_memberships = OrganizationMembership.objects.filter(is_active=True)
    for membership in user_memberships:
        if membership.days_duration == 0:
            membership.is_active = False
            membership.save()
            # TODO: get owner
            # owner = "example"
            # premium_subscription_over(membership.organization.owner)
        if membership.days_duration > 0:
            membership.days_duration -= 1
            membership.save()


@celery_app.task()
def premium_subscription_over(owner):
    email = owner.email
    template = MailTemplate.objects.get(pk=0)  # TODO: change to email template
    data = {  # TODO: change to owner data
        "organization_owner_name": owner.name,
    }
    replace_message_tags(template.message, data)
    send_email(email, template.subject, template.message)


@celery_app.task()
def wellcome_to_pro_plan(owner: User):
    email = owner.email
    template = MailTemplate.objects.get(pk=0)  # TODO: change to email template
    data = {  # TODO: change to owner data
        "organization_owner_name": owner.name,
    }
    message = replace_message_tags(template.message, data)
    send_email(email, template.subject, message)


@celery_app.task()
def wellcome_to_premium_plan(owner: User):
    email = owner.email
    template = MailTemplate.objects.get(pk=0)  # TODO: change to email template
    data = {  # TODO: change to owner data
        "organization_owner_name": owner.name,
    }
    message = replace_message_tags(template.message, data)
    send_email(email, template.subject, message)


@celery_app.task()
def attempt_to_activate_whatsapp(owner: User):
    # if owner is not premium
    email = owner.email
    template = MailTemplate.objects.get(pk=0)  #  TODO: change to email template
    data = {  # TODO: change to owner data
        "organization_owner_name": owner.name,
    }
    message = replace_message_tags(template.message, data)
    send_email(email, template.subject, message)


@celery_app.task()
def monthly_summary(owner: User):
    email = owner.email
    template = MailTemplate.objects.get(pk=0)  # TODO: change to email template
    data = {  # TODO: change to owner data
        "organization_owner_name": owner.name,
    }
    message = replace_message_tags(template.message, data)
    send_email(email, template.subject, message)
