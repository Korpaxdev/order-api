import django_filters

from backend.models import ProductModel, ProductShopModel


class ProductListFilterSet(django_filters.FilterSet):
    """Django filter set для модели ProductModel"""
    cat = django_filters.CharFilter(field_name="categories__name", lookup_expr="icontains")
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = ProductModel
        fields = ("id", "categories__name", "name")


class ProductShopFilterSet(django_filters.FilterSet):
    """Django filter set для модели ProductShopModel"""
    product_id = django_filters.NumberFilter(field_name="product__pk", lookup_expr="exact", label="Id товара")
    product_name = django_filters.CharFilter(field_name="product__name", lookup_expr="icontains")
    shop_id = django_filters.NumberFilter(field_name="shop__pk", lookup_expr="exact")
    shop_name = django_filters.CharFilter(field_name="shop__name", lookup_expr="icontains")
    category = django_filters.CharFilter(field_name="product__categories__name", lookup_expr="icontains")

    class Meta:
        model = ProductShopModel
        fields = {
            "price": ("lte", "gte", "lt", "gt"),
            "price_rrc": ("lte", "gte", "lt", "gt"),
            "quantity": ("lte", "gte", "lt", "gt"),
        }
