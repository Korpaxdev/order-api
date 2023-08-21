from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpRequest
from rest_framework import serializers
from rest_framework.reverse import reverse

from backend.models import OrderModel, ShopModel
from backend.serializers.user_serializers import (
    OrderDetailSerializer,
    OrderPositionSerializer,
    OrderProductShopSerializer,
    OrderSerializer,
)
from backend.utils.constants import ErrorMessages


class ShopListSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display")
    detail = serializers.HyperlinkedIdentityField("shop_detail", lookup_field="slug", lookup_url_kwarg="shop")

    class Meta:
        model = ShopModel
        fields = ("id", "name", "status", "detail")


class ShopDetailSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display")
    price_list = serializers.HyperlinkedIdentityField("shop_price_list", lookup_field="slug", lookup_url_kwarg="shop")
    orders = serializers.HyperlinkedIdentityField("shop_orders", lookup_field="slug", lookup_url_kwarg="shop")

    def __init__(self, instance: ShopModel, **kwargs):
        context = kwargs["context"]
        request: HttpRequest = context["request"]
        if not instance.status:
            del self.fields["price_list"]
        if not instance.is_manager_or_admin(request.user):
            del self.fields["price_file"]
        super().__init__(instance, **kwargs)

    class Meta:
        model = ShopModel
        fields = ("id", "name", "email", "phone", "status", "price_list", "price_file", "orders")


class ShopUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopModel
        fields = ("status",)

    def validate_status(self, value):
        if value and not self.instance.price_file:
            status_name = dict(ShopModel.SHOP_STATUS_CHOICES).get(value)
            raise serializers.ValidationError(ErrorMessages.CANT_SET_STATUS % status_name)
        return value


class ShopPriceFileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopModel
        fields = ("price_file",)
        extra_kwargs = {"price_file": {"required": True, "allow_null": False}}

    def validate_price_file(self, value: InMemoryUploadedFile):
        instance: ShopModel = self.instance
        if not instance.is_valid_price_file(value):
            raise serializers.ValidationError(ErrorMessages.PRICE_FILE_INCORRECT_FORMAT)
        return value


class ShopOrderSerializer(OrderSerializer):
    details = serializers.SerializerMethodField("get_details_url")

    def get_details_url(self, instance: OrderModel):
        view = self.context["view"]
        return reverse(
            "shop_order_details",
            request=self.context["request"],
            kwargs={"shop": view.kwargs.get(view.lookup_url_kwarg), "order": instance.pk},
        )


class ShopOrderDetailsSerializer(OrderDetailSerializer):
    items = serializers.SerializerMethodField("get_items_url")

    class Meta(OrderDetailSerializer.Meta):
        fields = ("id", "created_at", "status", "address", "items")

    def get_items_url(self, instance: OrderModel):
        view = self.context["view"]
        return reverse(
            "shop_order_items",
            request=self.context["request"],
            kwargs={"shop": view.kwargs.get(view.lookup_shop_url_kwarg), "order": instance.pk},
        )


class ShopOrderPositionSerializer(OrderProductShopSerializer):
    class Meta(OrderProductShopSerializer.Meta):
        fields = ("product_id", "product_name", "description", "params")


class ShopOrderItemsSerializer(OrderPositionSerializer):
    position = ShopOrderPositionSerializer(read_only=True)

    class Meta(OrderPositionSerializer.Meta):
        fields = ("position", "quantity", "price", "price_rrc")
