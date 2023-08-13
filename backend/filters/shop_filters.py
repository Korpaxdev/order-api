import django_filters

from backend.models import ProductShopModel, ShopModel


class ShopListFilterSet(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    status = django_filters.CharFilter(field_name="status", lookup_expr="icontains")

    class Meta:
        model = ShopModel
        fields = ("name", "status")


class ShopPriceListFilterSet(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="product__name", lookup_expr="icontains")
    cat = django_filters.CharFilter(field_name="product__categories__name", lookup_expr="icontains")

    class Meta:
        model = ProductShopModel
        fields = {
            "price": ("lte", "gte", "lt", "gt"),
            "price_rrc": ("lte", "gte", "lt", "gt"),
            "quantity": ("lte", "gte", "lt", "gt"),
        }
