from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

from backend.models import OrderModel, PasswordResetTokenModel, ShopModel, UserModel
from backend.utils.constants import EmailBaseSetup, EmailSendConfig, get_current_domain


def send_email(base_setup: EmailBaseSetup, to: list | tuple, context: dict):
    """Отправляет html email пользователям из списка to"""
    message = EmailMultiAlternatives(subject=base_setup.subject, from_email=settings.EMAIL_HOST_USER, to=to)
    html_body = render_to_string(template_name=base_setup.template, context=context)
    message.attach_alternative(html_body, "text/html")
    message.send()
    print(f"Message successfully sent to {to}")


@shared_task
def send_status_change_email(order_id: int):
    """Создает контекст для change_order_status.html и отправляет сообщение пользователю из OrderModel"""
    order = OrderModel.objects.get(id=order_id)
    user = order.user
    context = {
        "username": user.username,
        "order_id": order.pk,
        "status": order.get_status_display(),
        "url": f"http://{get_current_domain()}{reverse('profile')}",
    }
    send_email(EmailSendConfig.STATUS_CHANGE, to=(user.email,), context=context)


@shared_task
def send_password_reset_email(password_reset_id: int):
    """Создает контекст для password_reset.html и отправляет сообщение пользователю из PasswordResetTokenModel"""
    password_reset = PasswordResetTokenModel.objects.get(id=password_reset_id)
    context = {
        "url": f"http://{get_current_domain()}{reverse('password_update', kwargs={'user': password_reset.user.username, 'token': password_reset.token})}",
        "expire": password_reset.expire,
    }
    send_email(EmailSendConfig.PASSWORD_RESET, to=(password_reset.user.email,), context=context)


@shared_task
def send_price_success_updated_email(user_id: int, shop_id: int):
    """Создает контекст для password_success_update.html и отправляет сообщение пользователю из UserModel"""
    user = UserModel.objects.get(pk=user_id)
    shop = ShopModel.objects.get(pk=shop_id)
    context = {
        "url": f"http://{get_current_domain()}{shop.get_products_url()}",
        "username": user.username,
        "shop": shop.name,
    }
    send_email(EmailSendConfig.PRICE_UPDATE, to=(user.email,), context=context)


@shared_task
def send_price_error_update_email(user_id: int, shop_id: int, error_message: str):
    """Создает контекст для price_update_error.html и отправляет сообщение пользователю из UserModel"""
    user = UserModel.objects.get(pk=user_id)
    shop = ShopModel.objects.get(pk=shop_id)
    context = {
        "error_message": error_message,
        "username": user.username,
        "shop": shop.name,
    }
    send_email(EmailSendConfig.PRICE_UPDATE_ERROR, to=(user.email,), context=context)


@shared_task
def send_new_order_email(order_id: int):
    """Создает контекст для new_order.html и отправляет сообщение пользователю из UserModel"""
    order = OrderModel.objects.get(pk=order_id)
    context = {
        "order_id": order_id,
        "user": order.user.username,
        "url": f"http://{get_current_domain()}{order.get_admin_url()}",
    }
    send_email(EmailSendConfig.NEW_ORDER, to=(settings.ADMIN_EMAIL,), context=context)
