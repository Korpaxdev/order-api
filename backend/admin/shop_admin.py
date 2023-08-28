from django import forms
from django.contrib import admin

from backend.models import ShopModel


# ---------- Form Classes ----------

class ShopForm(forms.ModelForm):
    """Model Form для модели ShopModel"""

    class Meta:
        model = ShopModel
        fields = ("name", "price_file", "status", "email", "phone", "slug")

    def clean(self):
        """Валидация полей price_file и status
        Условие валидации: Невозможно установить status в True если у экземпляра ShopModel пустое поле price_file
        """
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        status_name = dict(ShopModel.SHOP_STATUS_CHOICES).get(status)
        if status and not cleaned_data.get("price_file"):
            self.add_error(
                "status", f"Невозможно установить статус {status_name}, когда у магазина отсутствует прайс файл"
            )


# ---------- Admin classes ----------

@admin.register(ShopModel)
class ShopAdmin(admin.ModelAdmin):
    """Model Admin для модели ShopModel"""

    list_display = ("id", "name", "status")
    readonly_fields = ("slug",)
    search_fields = ("name",)
    form = ShopForm
    list_display_links = ("id", "name")
