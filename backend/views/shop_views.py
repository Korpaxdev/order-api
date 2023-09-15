from django.http import HttpRequest
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import exceptions, generics, permissions
from rest_framework.response import Response

from backend.filters.order_filters import OrderListFilterSet
from backend.filters.shop_filters import ShopListFilterSet, ShopProductFilterSet
from backend.models import OrderItemModel, OrderModel, ProductShopModel, ShopModel
from backend.permissions.shop_permissions import IsManagerOrAdminPermission
from backend.serializers.product_serializers import ProductShopDetailListSerializer
from backend.serializers.shop_serializers import (ShopDetailSerializer, ShopListSerializer, ShopOrderDetailsSerializer,
                                                  ShopOrderItemsSerializer, ShopOrderSerializer,
                                                  ShopPriceFileUpdateSerializer, ShopUpdateStatusSerializer)
from backend.tasks import remove_file_task, update_price_file_task


class ShopListView(generics.ListAPIView):
    """View класс для представления списка объектов из модели ShopModel
    Url: shops/
    """

    serializer_class = ShopListSerializer
    queryset = ShopModel.objects.all()
    filterset_class = ShopListFilterSet


class ShopDetailView(generics.RetrieveAPIView):
    """View класс для детального представления объекта из модели ShopModel
    Url: shops/<slug:shop>/"""

    serializer_class = ShopDetailSerializer
    queryset = ShopModel.objects.all()
    lookup_field = "slug"
    lookup_url_kwarg = "shop"


class ShopPriceListView(generics.ListAPIView):
    """View класс для представления списка объектов ProductShop
    Url: shops/<slug:shop>/products/"""

    serializer_class = ProductShopDetailListSerializer
    filterset_class = ShopProductFilterSet
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
    """View класс для обновления поля status у модели ShopModel
    Url: shops/<slug:shop>/status/"""

    permission_classes = (permissions.IsAuthenticated, IsManagerOrAdminPermission)
    queryset = ShopModel.objects.all()
    serializer_class = ShopUpdateStatusSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "shop"


class ShopPriceFileUpdate(generics.GenericAPIView):
    """View класс для обновления поля price_file у модели ShopModel
    Url: shops/<slug:shop>/update/"""

    permission_classes = (permissions.IsAuthenticated, IsManagerOrAdminPermission)
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
    """View класс для представления списка объектов модели OrderModel, но с фильтрацией по shop__slug
    Url: shops/<slug:shop>/orders/"""

    permission_classes = (permissions.IsAuthenticated, IsManagerOrAdminPermission)
    serializer_class = ShopOrderSerializer
    filterset_class = OrderListFilterSet
    lookup_url_kwarg = "shop"
    lookup_field = "slug"

    def get_queryset(self):
        return OrderModel.objects.filter(items__position__shop__slug=self.kwargs.get(self.lookup_url_kwarg)).distinct()


class ShopOrderDetailsView(generics.RetrieveAPIView):
    """View класс для преставления детальной информации объекта модели OrderModel
    Url: shops/<slug:shop>/orders/<int:order>/"""

    permission_classes = (permissions.IsAuthenticated, IsManagerOrAdminPermission)
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
    """View класс для представления списка объектов модели OrderItem
    Url: shops/<slug:shop>/orders/<int:order>/items/"""

    permission_classes = (permissions.IsAuthenticated, IsManagerOrAdminPermission)
    serializer_class = ShopOrderItemsSerializer
    lookup_url_kwarg = "order"
    lookup_shop_url_kwarg = "shop"

    def get_queryset(self):
        return (
            OrderItemModel.objects.filter(
                order=self.kwargs.get(self.lookup_url_kwarg),
                position__shop__slug=self.kwargs.get(self.lookup_shop_url_kwarg),
            )
            .select_related("position__product", "position__shop")
            .prefetch_related("position__product__categories", "position__product_parameters__param")
        )
