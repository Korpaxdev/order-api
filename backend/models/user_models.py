import uuid
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from backend.models import ShopModel


class UserModel(AbstractUser):
    def is_manager(self, shop: ShopModel):
        return UserManagerModel.objects.filter(user=self, shops=shop).exists()


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
    NEW = "new"
    CONFIRMED = "confirmed"
    ASSEMBLED = "assembled"
    SENT = "sent"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    ORDER_STATUS_CHOICES = (
        (NEW, "Новый"),
        (CONFIRMED, "Подтвержден"),
        (ASSEMBLED, "Собран"),
        (SENT, "Отправлен"),
        (DELIVERED, "Доставлен"),
        (CANCELLED, "Отменен"),
    )

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="orders", verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default="new", verbose_name="Статус заказа")
    address = models.ForeignKey(OrderAddressModel, on_delete=models.PROTECT, verbose_name="Адрес доставки")
    additional = models.TextField(blank=True, null=True, verbose_name="Дополнительная информация")

    class Meta:
        verbose_name = "Заказ пользователя"
        verbose_name_plural = "Заказы пользователей"

    def delete(self, using=None, keep_parents=False):
        self.restore_items_quantity_for_position()
        super().delete(using, keep_parents)

    def restore_items_quantity_for_position(self):
        for item in self.items.all():
            item.restore_quantity_for_position()

    def remove_items_quantity_from_position(self):
        for item in self.items.all():
            item.remove_quantity_from_position()

    def get_total_price(self):
        return sum([item.get_sum_price() for item in self.items.all()])

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"order": self.pk})

    def __str__(self):
        return f"Заказ пользователя {self.user.username}"


class OrderItemsModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name="items", verbose_name="Заказ")
    position = models.ForeignKey(
        "ProductShopModel", related_name="order_items", on_delete=models.PROTECT, verbose_name="Позиция"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    price = models.PositiveIntegerField(verbose_name="Цена")
    price_rrc = models.PositiveIntegerField(verbose_name="РРЦ")

    class Meta:
        verbose_name = "Позиция"
        verbose_name_plural = "Позиции"
        unique_together = ("order", "position")

    def get_sum_price(self):
        return self.position.price * self.quantity

    def save(self, *args, **kwargs):
        self.price = self.position.price
        self.price_rrc = self.position.price_rrc
        if not self.pk:
            self.remove_quantity_from_position()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.restore_quantity_for_position()
        super().delete(*args, **kwargs)

    def remove_quantity_from_position(self):
        self.position.quantity -= self.quantity
        self.position.save()

    def restore_quantity_for_position(self):
        self.position.quantity += self.quantity
        self.position.save()

    def __str__(self):
        return f"{self.position.product.name} - {self.position.shop.name} - {self.quantity}"


class PasswordResetTokenModel(models.Model):
    token = models.UUIDField(default=uuid.uuid4, verbose_name="Токен")
    user = models.ForeignKey(UserModel, verbose_name="Пользователь", on_delete=models.CASCADE)
    expire = models.DateTimeField(
        default=datetime.now() + settings.PASSWORD_TOKEN_RESET_LIFETIME, verbose_name="Истекает"
    )

    class Meta:
        verbose_name = "Токен для сброса пароля"
        verbose_name_plural = "Токены для сброса пароля"

    def __str__(self):
        return f"Токен для сброса пароля пользователя {self.user.username}"
