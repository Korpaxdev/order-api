from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

from backend.models import OrderModel, PasswordResetTokenModel, UserModel
from backend.utils.constants import SITE_DOMAIN, EmailBaseSetup, EmailSendConfig


def send_email(base_setup: EmailBaseSetup, to: list | tuple, context: dict):
    message = EmailMultiAlternatives(subject=base_setup.subject, from_email=settings.EMAIL_HOST_USER, to=to)
    html_body = render_to_string(template_name=base_setup.template, context=context)
    message.attach_alternative(html_body, "text/html")
    message.send()
    print(f"Message successfully sent to {to}")


@shared_task
def send_status_change_email(to_user_id: int, order_id: int):
    user = UserModel.objects.get(id=to_user_id)
    order = OrderModel.objects.get(id=order_id)
    context = {
        "username": user.username,
        "order_id": order.pk,
        "status": order.get_status_display(),
        "details": f"{SITE_DOMAIN}{order.get_absolute_url()}",
    }
    send_email(EmailSendConfig.STATUS_CHANGE, to=(user.email,), context=context)


@shared_task
def send_password_reset_email(password_reset_id: int):
    password_reset = PasswordResetTokenModel.objects.get(id=password_reset_id)
    context = {
        "url": f"{SITE_DOMAIN}{reverse('password_update', kwargs={'user': password_reset.user.username, 'token': password_reset.token})}",
        "expire": password_reset.expire,
    }
    send_email(EmailSendConfig.PASSWORD_RESET, to=(password_reset.user.email,), context=context)
