from django.conf import settings
from django.utils import timezone


def generate_token_expire_time():
    return timezone.localtime() + settings.PASSWORD_TOKEN_RESET_LIFETIME
