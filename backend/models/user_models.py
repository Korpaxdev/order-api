import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from backend.models import ShopModel
from backend.utils.user_utils import generate_token_expire_time


class UserModel(AbstractUser):
    """Модель пользователя"""

    def is_manager(self, shop: ShopModel) -> bool:
        """Валидация является ли UserModel instance менеджером instance ShopModel"""
        return UserManagerModel.objects.filter(user=self, shops=shop).exists()


class UserManagerModel(models.Model):
    """Модель менеджера"""

    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, verbose_name="Пользователь")
    shops = models.ManyToManyField("ShopModel", related_name="managers", verbose_name="Магазины")

    class Meta:
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджеры"

    def __str__(self):
        return self.user.username


class OrderAddressModel(models.Model):
    """Модель адреса для заказа"""

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
    """Модель заказа"""

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
        """При удалении заказа возвращает количество товаров в магазине из заказа"""
        self.restore_items_quantity_for_position()
        super().delete(using, keep_parents)

    def restore_items_quantity_for_position(self):
        """Возвращает количество для всех товаров в заказе в магазин"""
        for item in self.items.all():
            item.restore_quantity_for_position()

    def remove_items_quantity_from_position(self):
        """Удаляет количество для всех товаров в магазине на основе заказа"""
        for item in self.items.all():
            item.remove_quantity_from_position()

    def get_total_price(self):
        """Возвращает сумму для всех позиций в заказе"""
        return sum([item.get_sum_price() for item in self.items.all()])

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"order": self.pk})

    def get_admin_url(self):
        return reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name), args=(self.id,))

    def __str__(self):
        return f"Заказ пользователя {self.user.username}"


class OrderItemModel(models.Model):
    """Модель позиции в заказе"""

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

    def get_sum_price(self) -> int:
        """Возвращает сумму для позиции"""
        return self.position.price * self.quantity

    def save(self, *args, **kwargs):
        """При сохранении на основе позиции создаем price и price_rrc.
        Это нужно чтобы если поменяются эти поля у ProductShopModel в заказе они остались не измененными"""
        self.price = self.position.price
        self.price_rrc = self.position.price_rrc
        if not self.pk:
            self.remove_quantity_from_position()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """При удалении позиции в заказе возвращаем количество для ProductShopModel"""
        self.restore_quantity_for_position()
        super().delete(*args, **kwargs)

    def remove_quantity_from_position(self):
        """Убавляет количество товара с магазина на основе количества в заказе"""
        self.position.quantity -= self.quantity
        self.position.save()

    def restore_quantity_for_position(self):
        """Возвращает количество товара в магазине из заказа"""
        self.position.quantity += self.quantity
        self.position.save()

    def __str__(self):
        return f"{self.position.product.name} - {self.position.shop.name} - {self.quantity}"


class PasswordResetTokenModel(models.Model):
    """Модель токена сброса пароля"""

    token = models.UUIDField(default=uuid.uuid4, verbose_name="Токен")
    user = models.ForeignKey(UserModel, verbose_name="Пользователь", on_delete=models.CASCADE)
    expire = models.DateTimeField(default=generate_token_expire_time, verbose_name="Истекает")

    class Meta:
        verbose_name = "Токен для сброса пароля"
        verbose_name_plural = "Токены для сброса пароля"

    def __str__(self):
        return f"Токен для сброса пароля пользователя {self.user.username}"
