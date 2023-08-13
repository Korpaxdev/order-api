from django.contrib import admin

from backend.models import UserModel


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    fields = (
        "username",
        "password",
        "email",
        "first_name",
        "last_name",
        "is_superuser",
        "is_staff",
        "is_active",
        "date_joined",
        "last_login",
    )
