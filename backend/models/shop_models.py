from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.urls import reverse
from pytils.translit import slugify


def update_filename(instance: "ShopModel", filename: str):
    new_file_name = f"{instance.name}-{datetime.now().strftime('%d-%m-%Y_%H-%M-%S-%f')}{Path(filename).suffix}"
    return f"prices/{new_file_name}"


class ShopModel(models.Model):
    SHOP_STATUS_CHOICES = (
        (True, "Готов принимать заказы"),
        (False, "Не готов принимать заказы"),
    )

    name = models.CharField(max_length=51, unique=True, verbose_name="Название магазина")
    price_file = models.FileField(upload_to=update_filename, blank=True, null=True, verbose_name="Прайс файл магазина")
    status = models.BooleanField(default=False, choices=SHOP_STATUS_CHOICES, verbose_name="Статус магазина")
    email = models.EmailField(unique=True, verbose_name="Email магазина")
    phone = models.CharField(max_length=21, unique=True, verbose_name="Телефон магазина")
    slug = models.SlugField(unique=True, db_index=True, blank=True, null=True)

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ShopModel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shop_details", kwargs={"shop": self.slug})

    def get_products_url(self):
        return reverse("shop_price_list", kwargs={"shop": self.slug})

    @staticmethod
    def is_valid_price_file(price_file: InMemoryUploadedFile):
        extension = Path(price_file.name).suffix
        return extension in settings.PRICE_FILE_FORMATS

    def __str__(self):
        return self.name
