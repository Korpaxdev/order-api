from django.http import HttpRequest
from rest_framework import exceptions, generics
from rest_framework.response import Response

from backend.filters.shop_filters import ShopListFilterSet, ShopPriceListFilterSet
from backend.models import ProductShopModel, ShopModel
from backend.permissions.shop_permissions import IsManagerOrAdminPermission
from backend.serializers.shop_serializers import (
    ShopDetailSerializer,
    ShopListSerializer,
    ShopPriceFileUpdateSerializer,
    ShopPriceListSerializer,
    ShopUpdateStatusSerializer,
)
from backend.tasks import remove_file, update_price_file


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


class ShopPriceFileUpdate(generics.GenericAPIView):
    permission_classes = (IsManagerOrAdminPermission,)
    queryset = ShopModel.objects.all()
    serializer_class = ShopPriceFileUpdateSerializer
    lookup_field = "slug"

    def post(self, request: HttpRequest, slug: str):
        instance: ShopModel = self.get_object()
        serializer = self.serializer_class(instance=instance, data=self.request.data)
        if not serializer.is_valid():
            raise exceptions.ValidationError(serializer.errors)
        old_price_file = instance.price_file
        if old_price_file and old_price_file.name:
            remove_file.delay(old_price_file.path)
        serializer.save()
        update_price_file.delay(instance.pk, instance.price_file.path)
        return Response(serializer.data)
