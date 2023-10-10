from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from backend.models import (OrderAddressModel, OrderItemModel, OrderModel, PasswordResetTokenModel, ProductShopModel,
                            UserManagerModel, UserModel)
from backend.tasks.email_tasks import send_status_change_email
from backend.utils.constants import ErrorMessages


# ---------- Form Classes ----------
class OrderItemForm(forms.ModelForm):
    """Model Form для модели OrderItemModel"""

    class Meta:
        model = OrderItemModel
        fields = ("position", "quantity", "price", "price_rrc")

    def clean(self):
        """Валидация полей quantity и position
        Условия валидации
        1. quantity должен быть больше 0
        2. у position quantity должен быть больше 0
        3. quantity должен быть меньше чем position quantity
        """
        cleaned_data = self.cleaned_data
        quantity: int = cleaned_data.get("quantity")
        if not quantity:
            self.add_error("quantity", ErrorMessages.QUANTITY_GREATER_THAN_0)
        position: ProductShopModel | None = cleaned_data.get("position")
        if not position:
            return
        elif not position.quantity:
            self.add_error("position", ErrorMessages.POSITION_IS_OUT_OF_STOCK)
        elif position.quantity < quantity and self.initial.get("quantity") != quantity:
            self.add_error("quantity", ErrorMessages.LESSER_QUANTITY)
            self.add_error("position", ErrorMessages.LESSER_QUANTITY)


# ---------- Inline classes ----------


class OrderItemInline(admin.TabularInline):
    """Tabular Inline для модели OrderItemModel"""

    extra = 1
    model = OrderItemModel
    fields = ("position", "quantity", "price", "price_rrc", "get_total_price")
    readonly_fields = ("price", "price_rrc", "get_total_price")
    form = OrderItemForm
    raw_id_fields = ("position",)

    @admin.display(description="Итого")
    def get_total_price(self, instance: OrderItemModel) -> int:
        return instance.get_sum_price()


# ---------- Admin classes ----------


@admin.register(UserModel)
class UserModelAdmin(UserAdmin):
    """Model Admin для Модели UserModel"""

    search_fields = ("username", "email")
    list_display = ("username", "email", "is_superuser", "is_staff", "is_active")


@admin.register(UserManagerModel)
class UserManagerModelAdmin(admin.ModelAdmin):
    """Model Admin для модели UserManagerModel"""

    list_filter = ("shops",)
    list_display = ("get_user_name", "get_shops")
    search_fields = ("user__username",)

    @admin.display(description="Пользователь")
    def get_user_name(self, instance: UserManagerModel) -> str:
        return instance.user.username

    @admin.display(description="Магазины")
    def get_shops(self, instance: UserManagerModel) -> list[str]:
        return [shop.name for shop in instance.shops.all()]


@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    """Model Admin для модели OrderModel"""

    raw_id_fields = ("user", "address")
    inlines = (OrderItemInline,)
    list_display = ("id", "user", "status", "created_at", "get_total_price")
    list_display_links = ("id", "user")
    search_fields = ("user__username",)
    list_filter = ("status", "created_at")

    @admin.display(description="Итого")
    def get_total_price(self, instance: OrderModel) -> int:
        return instance.get_total_price()

    def delete_queryset(self, request, queryset):
        """Вызывается при множественном удалении. В нем мы вызываем метод delete у самой модели.
        По умолчанию при множественном удалении django не вызывает данный метод у модели"""
        for item in queryset:
            item.delete()

    def save_formset(self, request, form, formset, change):
        """В методе в зависимости от условия уменьшается количество товаров на складе или возвращается количество товара с заказа на склад
        Условия:
        1. Если новый status заказа отменен - то quantity с заказа возвращается в quantity позиции в магазине
        2. Если прошлый status заказа был отменен, а новый не отменен - то quantity с заказа списывается с quantity позиции в магазине
        3. Если было изменение quantity заказа, то в quantity позиции добавляется разница previous quantity заказа и текущий quantity заказа
        """
        if change:
            order_instance: OrderModel = form.instance
            if "status" in form.changed_data:
                send_status_change_email.delay(order_instance.pk)
                previous_status = form.initial.get("status")
                if order_instance.status == order_instance.CANCELLED:
                    order_instance.restore_items_quantity_for_position()
                elif previous_status == order_instance.CANCELLED and order_instance.status != previous_status:
                    order_instance.remove_items_quantity_from_position()
            for formset_form in formset.forms:
                instance: OrderItemModel = formset_form.instance
                if not instance.pk:
                    continue
                elif "quantity" in formset_form.changed_data and order_instance.status != order_instance.CANCELLED:
                    previous_quantity = formset_form.initial.get("quantity", 0)
                    instance.position.quantity += previous_quantity - instance.quantity
                    instance.position.save()

        super().save_formset(request, form, formset, change)


@admin.register(OrderAddressModel)
class OrderAddressModelAdmin(admin.ModelAdmin):
    """Model Admin для модели OrderAddressModel"""

    list_display = ("id", "postal_code", "country", "region", "city")
    list_display_links = ("id", "postal_code")


@admin.register(PasswordResetTokenModel)
class PasswordResetTokenModelAdmin(admin.ModelAdmin):
    """Model Admin для модели PasswordResetTokenModel"""

    readonly_fields = ("token", "user")
    list_display = ("pk", "user", "expire")
    list_display_links = ("pk", "user")
    search_fields = ("user__username", "pk")
    list_filter = ("expire",)
