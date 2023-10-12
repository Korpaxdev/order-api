from celery import shared_task
from django.conf import settings


@shared_task
def disable_send_email():
    settings.SEND_EMAIL = False
    print("SEND_EMAIL is False")
    return settings.SEND_EMAIL
