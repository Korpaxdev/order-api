from django.db import models
from pytils.translit import slugify


class CategoryModel(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    categories = models.ManyToManyField(CategoryModel, related_name="products", verbose_name="Категории")
    shops = models.ManyToManyField("ShopModel", through="ProductShopModel", verbose_name="Магазины")
    slug = models.SlugField(max_length=100, blank=True, null=True, unique=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductShopModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name="Товар")
    shop = models.ForeignKey("ShopModel", on_delete=models.CASCADE, related_name="positions", verbose_name="Магазин")
    description = models.TextField(blank=True, null=True, verbose_name="Описание товара")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.PositiveIntegerField(verbose_name="Цена")
    price_rrc = models.PositiveIntegerField(verbose_name="РРЦ")

    class Meta:
        verbose_name = "Товар в магазинах"
        verbose_name_plural = "Товары в магазинах"
        unique_together = ("product", "shop")

    def __str__(self):
        return f"{self.product.name} - {self.shop.name}"


class ParameterModel(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название параметра")

    class Meta:
        verbose_name = "Параметр"
        verbose_name_plural = "Параметры"

    def __str__(self):
        return self.name


class ProductParameterModel(models.Model):
    product = models.ForeignKey(
        ProductShopModel, on_delete=models.CASCADE, related_name="product_parameters", verbose_name="Товар"
    )
    param = models.ForeignKey(ParameterModel, on_delete=models.CASCADE, verbose_name="Параметр")
    value = models.CharField(max_length=50, verbose_name="Значение параметра")

    class Meta:
        verbose_name = "Параметр товара"
        verbose_name_plural = "Параметры товара"

    def __str__(self):
        return f"{self.product.product.name} - {self.param.name} - {self.value}"
