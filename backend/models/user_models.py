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
