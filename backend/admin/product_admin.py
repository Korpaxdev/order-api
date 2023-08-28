from django.contrib import admin

from backend.models import CategoryModel, ParameterModel, ProductModel, ProductParameterModel, ProductShopModel


# ---------- Inline classes ----------


class ProductParameterInline(admin.TabularInline):
    """Tabular Inline для модели ProductParameterModel"""

    model = ProductParameterModel
    extra = 1


# ---------- Admin classes ----------


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    """Model Admin для модели CategoryModel"""

    search_fields = ("name",)


@admin.register(ParameterModel)
class ProductParameterModelAdmin(admin.ModelAdmin):
    """Model Admin для модели ParameterModel"""

    search_fields = ("name",)


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    """Model Admin для модели ProductModel"""

    list_display = ("id", "name", "get_categories")
    readonly_fields = ("slug",)
    search_fields = ("name",)
    list_filter = ("categories",)
    list_display_links = ("id", "name")

    @admin.display(description="Категории")
    def get_categories(self, instance: ProductModel) -> list[str]:
        return [category.name for category in instance.categories.all()]


@admin.register(ProductShopModel)
class ProductShopModelAdmin(admin.ModelAdmin):
    """Model Admin для модели ProductShopModel"""

    list_display = (
        "get_product_id",
        "get_product_name",
        "get_categories",
        "get_shop_name",
        "quantity",
        "price",
        "price_rrc",
    )
    raw_id_fields = ("product", "shop")
    list_filter = ("product__categories", "shop__name")
    inlines = (ProductParameterInline,)
    search_fields = ("product__name", "shop__name")
    list_display_links = ("get_product_id", "get_product_name")

    @admin.display(description="Id товара")
    def get_product_id(self, instance: ProductShopModel) -> int:
        return instance.product.id

    @admin.display(description="Товар")
    def get_product_name(self, instance: ProductShopModel) -> str:
        return instance.product.name

    @admin.display(description="Категории")
    def get_categories(self, instance: ProductShopModel) -> list[str]:
        return [category.name for category in instance.product.categories.all()]

    @admin.display(description="Магазин")
    def get_shop_name(self, instance: ProductShopModel) -> str:
        return instance.shop.name
