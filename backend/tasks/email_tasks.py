from celery import shared_task
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from backend.models import ShopModel, UserModel


@shared_task
def send_email_task(user_id: int, shop_id: int, template: str):
    user = UserModel.objects.get(id=user_id)
    if not user.email:
        print(f"{user.username} doesn't have an email address")
        return
    shop = ShopModel.objects.get(id=shop_id)
    domain = Site.objects.get_current().domain

    message = EmailMultiAlternatives(subject="Обновление прайса", from_email=settings.EMAIL_HOST_USER, to=(user.email,))

    html_body = render_to_string(template, context={"shop": shop, "domain": domain})
    message.attach_alternative(html_body, "text/html")
    message.send()
    print(f"Message successfully sent to {user.username}")
