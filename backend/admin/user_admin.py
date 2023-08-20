from django.contrib import admin

from backend.models import OrderAddressModel, OrderItemsModel, OrderModel, UserManagerModel, UserModel

# ---------- Inline classes ----------


class OrderItemInline(admin.TabularInline):
    extra = 1
    model = OrderItemsModel
    fields = ("position", "quantity", "price", "price_rrc", "get_total_price")
    readonly_fields = ("price", "price_rrc", "get_total_price")

    @admin.display(description="Итого")
    def get_total_price(self, instance: OrderItemsModel):
        return instance.get_sum_price()


# ---------- Admin classes ----------


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
    search_fields = ("username", "email")
    list_display = ("username", "email", "is_superuser", "is_staff", "is_active")


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


@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    raw_id_fields = ("user", "address")
    inlines = (OrderItemInline,)
    list_display = ("id", "user", "status", "created_at", "get_total_price")
    list_display_links = ("id", "user")
    search_fields = ("user__username",)
    list_filter = ("status", "created_at")

    @admin.display(description="Итого")
    def get_total_price(self, instance: OrderModel):
        return instance.get_total_price()


@admin.register(OrderAddressModel)
class OrderAddressModelAdmin(admin.ModelAdmin):
    pass
