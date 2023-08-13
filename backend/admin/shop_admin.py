from django import forms
from django.contrib import admin

from backend.models import SHOP_STATUS_CHOICES, ShopModel


class ShopForm(forms.ModelForm):
    class Meta:
        model = ShopModel
        fields = ("name", "price_file", "status", "email", "phone", "slug")

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        status_name = dict(SHOP_STATUS_CHOICES).get(status)
        if status and not cleaned_data.get("price_file"):
            self.add_error(
                "status", f"Невозможно установить статус {status_name}, когда у магазина отсутствует прайс файл"
            )


@admin.register(ShopModel)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "status")
    readonly_fields = ("slug",)
    form = ShopForm