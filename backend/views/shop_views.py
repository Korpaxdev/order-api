from rest_framework import generics

from backend.filters.shop_filters import ShopListFilterSet, ShopPriceListFilterSet
from backend.models import ProductShopModel, ShopModel
from backend.serializers.shop_serializers import (
    ShopDetailSerializer,
    ShopListSerializer,
    ShopPriceListSerializer,
    ShopUpdateStatusSerializer,
)


class ShopListView(generics.ListAPIView):
    serializer_class = ShopListSerializer
    queryset = ShopModel.objects.all()
    filterset_class = ShopListFilterSet


class ShopDetailView(generics.RetrieveAPIView):
    serializer_class = ShopDetailSerializer
    queryset = ShopModel.objects.all()
    lookup_field = "slug"


class ShopPriceListView(generics.ListAPIView):
    serializer_class = ShopPriceListSerializer
    filterset_class = ShopPriceListFilterSet
    lookup_field = "slug"

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_field)
        return (
            ProductShopModel.objects.filter(shop__slug=slug, shop__status=True, quantity__gt=0)
            .select_related("product", "shop")
            .prefetch_related("product_parameters__param", "product__categories")
        )


class ShopUpdateStatusView(generics.UpdateAPIView):
    queryset = ShopModel.objects.all()
    serializer_class = ShopUpdateStatusSerializer
    lookup_field = "slug"
