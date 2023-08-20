from django import forms
from django.contrib import admin

from backend.models import OrderAddressModel, OrderItemsModel, OrderModel, ProductShopModel, UserManagerModel, UserModel
from backend.tasks.email_tasks import send_status_change_email
from backend.utils.constants import ErrorMessages


# ---------- Form Classes ----------
class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItemsModel
        fields = ("position", "quantity", "price", "price_rrc")

    def clean(self):
        cleaned_data = self.cleaned_data
        quantity: int = cleaned_data.get("quantity")
        if not quantity:
            self.add_error("quantity", ErrorMessages.QUANTITY_GREATER_THAN_0)
        position: ProductShopModel | None = cleaned_data.get("position")
        if not position:
            return
        elif not position.quantity:
            self.add_error("position", ErrorMessages.POSITION_IS_OUT_OF_STOCK)
        elif position.quantity < quantity:
            self.add_error("quantity", ErrorMessages.LESSER_QUANTITY)
            self.add_error("position", ErrorMessages.LESSER_QUANTITY)


# ---------- Inline classes ----------


class OrderItemInline(admin.TabularInline):
    extra = 1
    model = OrderItemsModel
    fields = ("position", "quantity", "price", "price_rrc", "get_total_price")
    readonly_fields = ("price", "price_rrc", "get_total_price")
    form = OrderItemForm
    raw_id_fields = ("position",)

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

    def save_model(self, request, obj, form, change):
        if change and "status" in form.changed_data:
            send_status_change_email.delay(request.user.pk, obj.pk)
        super(OrderModelAdmin, self).save_model(request, obj, form, change)


@admin.register(OrderAddressModel)
class OrderAddressModelAdmin(admin.ModelAdmin):
    list_display = ("id", "postal_code", "country", "region", "city")
    list_display_links = ("id", "postal_code")
