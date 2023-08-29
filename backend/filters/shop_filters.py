import django_filters

from backend.models import ProductShopModel, ShopModel


class ShopListFilterSet(django_filters.FilterSet):
    """Django filter set для модели ShopModel"""

    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    status = django_filters.CharFilter(field_name="status", lookup_expr="icontains")

    class Meta:
        model = ShopModel
        fields = ("name", "status")


class ShopProductFilterSet(django_filters.FilterSet):
    """Django filter set для модели ProductShopModel"""

    product_id = django_filters.NumberFilter(field_name="product__pk", lookup_expr="exact", label="Id товара")
    product_name = django_filters.CharFilter(field_name="product__name", lookup_expr="icontains")
    category = django_filters.CharFilter(field_name="product__categories__name", lookup_expr="icontains")

    class Meta:
        model = ProductShopModel
        fields = {
            "price": ("lte", "gte", "lt", "gt"),
            "price_rrc": ("lte", "gte", "lt", "gt"),
            "quantity": ("lte", "gte", "lt", "gt"),
        }
