from django.contrib.auth.models import AbstractUser
from django.db import models


class UserModel(AbstractUser):
    pass


class UserManagerModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, verbose_name="Пользователь")
    shops = models.ManyToManyField("ShopModel", related_name="managers", verbose_name="Магазины")

    class Meta:
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджеры"

    def __str__(self):
        return self.user.username


class OrderAddressModel(models.Model):
    postal_code = models.IntegerField(verbose_name="Почтовый индекс")
    country = models.CharField(max_length=100, verbose_name="Страна")
    region = models.CharField(max_length=100, verbose_name="Область")
    city = models.CharField(max_length=100, verbose_name="Населенный пункт")

    class Meta:
        verbose_name = "Адрес доставки"
        verbose_name_plural = "Адреса доставок"

    def __str__(self):
        return f"{self.country} - {self.city} - {self.postal_code}"


class OrderModel(models.Model):
    ORDER_STATUS_CHOICES = (
        ("new", "Новый"),
        ("confirmed", "Подтвержден"),
        ("assembled", "Собран"),
        ("sent", "Отправлен"),
        ("delivered", "Доставлен"),
        ("canceled", "Отменен"),
    )

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="orders", verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default="new", verbose_name="Статус заказа")
    address = models.ForeignKey(OrderAddressModel, on_delete=models.PROTECT, verbose_name="Адрес доставки")
    additional = models.TextField(blank=True, null=True, verbose_name="Дополнительная информация")

    class Meta:
        verbose_name = "Заказ пользователя"
        verbose_name_plural = "Заказы пользователей"

    def __str__(self):
        return f"Заказ пользователя {self.user.username}"

    def get_total_price(self):
        return sum([item.get_sum_price() for item in self.items.all()])


class OrderItemsModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name="items", verbose_name="Заказ")
    position = models.ForeignKey("ProductShopModel", on_delete=models.PROTECT, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество товара")
    price = models.PositiveIntegerField(verbose_name="Цена товара")
    price_rrc = models.PositiveIntegerField(verbose_name="Рекомендованная розничная цена")

    class Meta:
        verbose_name = "Позиция"
        verbose_name_plural = "Позиции"
        unique_together = ("order", "position")

    def get_sum_price(self):
        return self.position.price * self.quantity

    def save(self, *args, **kwargs):
        self.price = self.position.price
        self.price_rrc = self.position.price_rrc
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.position.product.name} - {self.position.shop.name} - {self.quantity}"
