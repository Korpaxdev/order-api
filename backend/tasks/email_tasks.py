from celery import shared_task
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

from backend.models import OrderModel, UserModel, PasswordResetTokenModel


def send_email(subject: str, to: list | tuple, context: dict, template: str):
    message = EmailMultiAlternatives(subject=subject, from_email=settings.EMAIL_HOST_USER, to=to)
    html_body = render_to_string(template, context=context)
    message.attach_alternative(html_body, "text/html")
    message.send()
    print(f"Message successfully sent to {to}")


@shared_task
def send_status_change_email(to_user_id: int, order_id: int):
    subject = "Ваш статус заказа был изменен"
    template = "email_templates/change_order_status.html"
    user = UserModel.objects.get(id=to_user_id)
    order = OrderModel.objects.get(id=order_id)
    domain = Site.objects.get_current().domain
    context = {
        "username": user.username,
        "order_id": order.pk,
        "status": order.get_status_display(),
        "details": f"{domain}{order.get_absolute_url()}",
    }
    send_email(subject=subject, to=(user.email,), context=context, template=template)


@shared_task
def send_password_reset_email(password_reset_id: int):
    subject = "Сброс пароля"
    template = 'email_templates/password_reset.html'
    password_reset = PasswordResetTokenModel.objects.get(id=password_reset_id)
    domain = Site.objects.get_current().domain
    context = {
        'url': f"{domain}{reverse('password_update', kwargs={'user': password_reset.user.username, 'token': password_reset.token})}",
        "expire": password_reset.expire,
    }
    send_email(subject=subject, to=(password_reset.user.email,), context=context, template=template)
