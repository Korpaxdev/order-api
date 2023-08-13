from django.db import models
from pytils.translit import slugify

SHOP_STATUS_CHOICES = (
    (True, "Готов принимать заказы"),
    (False, "Не готов принимать заказы"),
)


class ShopModel(models.Model):
    name = models.CharField(max_length=51, unique=True, verbose_name="Название магазина")
    price_file = models.FileField(upload_to="prices", blank=True, null=True, verbose_name="Прайс файл магазина")
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

    def __str__(self):
        return self.name
