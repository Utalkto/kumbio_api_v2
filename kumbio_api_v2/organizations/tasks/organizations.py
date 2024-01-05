from celery.schedules import crontab
from kumbio_api_v2.users.models import User

from config import celery_app

# templates
from kumbio_api_v2.communications.models.templates import MailTemplate

# communications
from kumbio_api_v2.communications.notification import replace_message_tags, send_email

# Models
from kumbio_api_v2.organizations.models import OrganizationMembership


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(day_of_week="*", hour=00, minute=00),
        check_organization_memberships,
        name="check_organization_memberships",
    )
    sender.add_periodic_task(
        crontab(day_of_month="1", hour=00, minute=00),
        monthly_summary,
        name="monthly_summary",
    )


@celery_app.task
def check_organization_memberships():
    """Check user memberships"""
    user_memberships = OrganizationMembership.objects.filter(is_active=True)
    for membership in user_memberships:
        if membership.days_duration == 0:
            membership.is_active = False
            membership.save()
            owner = membership.organization.owner
            premium_subscription_over(owner)
        if membership.days_duration > 0:
            membership.days_duration -= 1
            membership.save()


@celery_app.task()
def premium_subscription_over(owner):
    email = owner.email
    template = MailTemplate.objects.get(pk=13)  # TODO: change to email template
    data = {  # TODO: change to owner data
        "organization_owner_name": owner.name,
    }
    replace_message_tags(template.message, data)
    send_email(email, template.subject, template.message)


@celery_app.task()
def wellcome_to_pro_plan(owner: User):
    # TODO: use this task when user buy a pro plan
    email = owner.email
    template = MailTemplate.objects.get(pk=0)  # TODO: change to email template
    data = {
        "organization_owner_name": owner.name,
    }
    message = replace_message_tags(template.message, data)
    send_email(email, template.subject, message)


@celery_app.task()
def wellcome_to_premium_plan(owner: User):
    # TODO: use this task when user buy a premium plan
    email = owner.email
    template = MailTemplate.objects.get(pk=0)  # TODO: change to email template
    data = {  # TODO: change to owner data
        "organization_owner_name": owner.name,
    }
    message = replace_message_tags(template.message, data)
    send_email(email, template.subject, message)


@celery_app.task()
def attempt_to_activate_whatsapp(owner: User):
    # TODO: use this task when user try to activate whatsapp
    # if owner is not premium
    email = owner.email
    # Change to email template
    template = MailTemplate.objects.get(pk=0)
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
