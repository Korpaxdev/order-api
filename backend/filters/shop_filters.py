import django_filters

from backend.models import ShopModel


class ShopListFilterSet(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    status = django_filters.CharFilter(field_name="status", lookup_expr="icontains")

    class Meta:
        model = ShopModel
        fields = ("name", "status")
