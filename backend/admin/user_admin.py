from django.contrib import admin

from backend.models import UserManagerModel, UserModel


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


@admin.register(UserManagerModel)
class UserManagerModelAdmin(admin.ModelAdmin):
    list_filter = ("shops",)
    list_display = ("get_user_name", "get_shops")
    search_fields = ("user__username",)

    @admin.display(description="Пользователь")
    def get_user_name(self, instance: UserManagerModel):
        return instance.user.username

    @admin.display(description="Магазины")
    def get_shops(self, instance: UserManagerModel):
        return [shop.name for shop in instance.shops.all()]
