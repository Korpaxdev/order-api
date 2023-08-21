from django.http import HttpRequest
from rest_framework import exceptions, generics, permissions
from rest_framework.response import Response

from backend.filters.product_filters import ProductShopFilterSet
from backend.filters.shop_filters import ShopListFilterSet
from backend.models import OrderItemsModel, OrderModel, ProductShopModel, ShopModel
from backend.permissions.shop_permissions import IsManagerOrAdminPermission
from backend.serializers.product_serializers import ProductShopDetailListSerializer
from backend.serializers.shop_serializers import (
    ShopDetailSerializer,
    ShopListSerializer,
    ShopOrderDetailsSerializer,
    ShopOrderItemsSerializer,
    ShopOrderSerializer,
    ShopPriceFileUpdateSerializer,
    ShopUpdateStatusSerializer,
)
from backend.tasks import remove_file_task, update_price_file_task


class ShopListView(generics.ListAPIView):
    serializer_class = ShopListSerializer
    queryset = ShopModel.objects.all()
    filterset_class = ShopListFilterSet


class ShopDetailView(generics.RetrieveAPIView):
    serializer_class = ShopDetailSerializer
    queryset = ShopModel.objects.all()
    lookup_field = "slug"
    lookup_url_kwarg = "shop"


class ShopPriceListView(generics.ListAPIView):
    serializer_class = ProductShopDetailListSerializer
    filterset_class = ProductShopFilterSet
    lookup_field = "slug"
    lookup_url_kwarg = "shop"

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        return (
            ProductShopModel.objects.filter(shop__slug=slug, shop__status=True, quantity__gt=0)
            .select_related("product", "shop")
            .prefetch_related("product_parameters__param", "product__categories")
        )


class ShopUpdateStatusView(generics.UpdateAPIView):
    queryset = ShopModel.objects.all()
    serializer_class = ShopUpdateStatusSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "shop"


class ShopPriceFileUpdate(generics.GenericAPIView):
    permission_classes = (IsManagerOrAdminPermission,)
    queryset = ShopModel.objects.all()
    serializer_class = ShopPriceFileUpdateSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "shop"

    def post(self, request: HttpRequest, shop: str):
        instance: ShopModel = self.get_object()
        serializer = self.serializer_class(instance=instance, data=self.request.data)
        if not serializer.is_valid():
            raise exceptions.ValidationError(serializer.errors)
        old_price_file = instance.price_file
        if old_price_file and old_price_file.name:
            remove_file_task.delay(old_price_file.path)
        serializer.save()
        update_price_file_task.delay(instance.pk, instance.price_file.path, request.user.pk)
        return Response(serializer.data)


class ShopOrderView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ShopOrderSerializer
    lookup_url_kwarg = "shop"
    lookup_field = "slug"

    def get_queryset(self):
        return OrderModel.objects.filter(items__position__shop__slug=self.kwargs.get(self.lookup_url_kwarg)).distinct()


class ShopOrderDetailsView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ShopOrderDetailsSerializer
    lookup_url_kwarg = "order"
    lookup_shop_url_kwarg = "shop"

    def get_queryset(self):
        return (
            OrderModel.objects.filter(items__position__shop__slug=self.kwargs.get(self.lookup_shop_url_kwarg))
            .prefetch_related("items__position")
            .distinct()
        )


class ShopOrderItemsView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ShopOrderItemsSerializer
    lookup_url_kwarg = "order"
    lookup_shop_url_kwarg = "shop"

    def get_queryset(self):
        return (
            OrderItemsModel.objects.filter(
                order=self.kwargs.get(self.lookup_url_kwarg),
                position__shop__slug=self.kwargs.get(self.lookup_shop_url_kwarg),
            )
            .select_related("position__product", "position__shop")
            .prefetch_related("position__product__categories", "position__product_parameters__param")
        )
