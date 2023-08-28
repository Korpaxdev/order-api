import django_filters

from backend.models import OrderModel


class OrderListFilterSet(django_filters.FilterSet):
    """Django filter set для модели OrderModel"""

    class Meta:
        model = OrderModel
        fields = {
            "id": ("exact",),
            "status": ("icontains",),
            "created_at": ("lte", "gte", "lt", "gt")
        }
