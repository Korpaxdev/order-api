from celery import shared_task
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from backend.models import OrderModel, UserModel


def send_email_task(subject: str, to: list | tuple, context: dict, template: str):
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
    send_email_task(subject=subject, to=(user.email,), context=context, template=template)
