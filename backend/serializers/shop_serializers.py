from django.core.files.uploadedfile import InMemoryUploadedFile
from drf_spectacular.utils import OpenApiExample, extend_schema_field, extend_schema_serializer
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.reverse import reverse

from backend.models import OrderModel, ShopModel, UserModel
from backend.serializers.user_serializers import (
    OrderDetailSerializer,
    OrderPositionSerializer,
    OrderProductShopSerializer,
    OrderSerializer,
)
from backend.utils.constants import ErrorMessages


class ShopListSerializer(serializers.ModelSerializer):
    """Serializer для списка модели ShopModel"""

    status = serializers.CharField(source="get_status_display")
    detail = serializers.HyperlinkedIdentityField("shop_details", lookup_field="slug", lookup_url_kwarg="shop")

    class Meta:
        model = ShopModel
        fields = ("id", "name", "status", "detail")


class ShopDetailSerializer(serializers.ModelSerializer):
    """Serializer для модели ShopModel.
    Представляет более детальную информацию по магазину"""

    status = serializers.CharField(source="get_status_display")
    price_list = serializers.HyperlinkedIdentityField("shop_price_list", lookup_field="slug", lookup_url_kwarg="shop")
    orders = serializers.HyperlinkedIdentityField("shop_orders", lookup_field="slug", lookup_url_kwarg="shop")

    def __init__(self, instance: ShopModel = None, data=empty, **kwargs):
        """Удаляем поля из модели если:
        1. У магазина статус не готов - удаляем price_file
        2. Если пользователь не админ или не менеджер магазина - удаляем price_file и orders"""
        super().__init__(instance, data, **kwargs)
        user: UserModel = self.context["request"].user
        if instance and not instance.status:
            del self.fields["price_list"]
        if user.is_anonymous or (not user.is_manager(instance) and not user.is_superuser):
            del self.fields["price_file"]
            del self.fields["orders"]

    class Meta:
        model = ShopModel
        fields = ("id", "name", "email", "phone", "status", "price_list", "price_file", "orders")


class ShopUpdateStatusSerializer(serializers.ModelSerializer):
    """Serializer для модели ShopModel. Представляет обновления статуса магазина"""

    class Meta:
        model = ShopModel
        fields = ("status",)
        extra_kwargs = {"status": {"required": True, "allow_null": False}}

    def validate_status(self, value):
        """Валидация статуса магазина.
        Статус невозможно установить готов если у магазина не загружен прайс файл"""
        if value and not self.instance.price_file:
            status_name = dict(ShopModel.SHOP_STATUS_CHOICES).get(value)
            raise serializers.ValidationError(ErrorMessages.CANT_SET_STATUS % status_name)
        return value


class ShopPriceFileUpdateSerializer(serializers.ModelSerializer):
    """Serializer для модели ShopModel. Представляет обновление price_file"""

    class Meta:
        model = ShopModel
        fields = ("price_file",)
        extra_kwargs = {"price_file": {"required": True, "allow_null": False}}

    def validate_price_file(self, value: InMemoryUploadedFile):
        """Валидация прайс файла на основе доступных расширений"""
        instance: ShopModel = self.instance
        if not instance.is_valid_price_file(value):
            raise serializers.ValidationError(ErrorMessages.PRICE_FILE_INCORRECT_FORMAT)
        return value


class ShopOrderSerializer(OrderSerializer):
    """Serializer для модели OrderModel.
    Состоит из обычного OrderSerializer, только изменены ссылки на детальную информацию"""

    details = serializers.SerializerMethodField("get_details_url")

    @extend_schema_field(serializers.CharField)
    def get_details_url(self, instance: OrderModel):
        view = self.context["view"]
        return reverse(
            "shop_order_details",
            request=self.context["request"],
            kwargs={"shop": view.kwargs.get(view.lookup_url_kwarg), "order": instance.pk},
        )


class ShopOrderDetailsSerializer(OrderDetailSerializer):
    """Serializer для модели OrderModel.
    Состоит из обычного OrderDetailSerializer. Только изменены ссылки на items"""

    items = serializers.SerializerMethodField("get_items_url")

    class Meta(OrderDetailSerializer.Meta):
        fields = ("id", "created_at", "status", "address", "items")

    @extend_schema_field(serializers.CharField)
    def get_items_url(self, instance: OrderModel):
        view = self.context["view"]
        return reverse(
            "shop_order_items",
            request=self.context["request"],
            kwargs={"shop": view.kwargs.get(view.lookup_shop_url_kwarg), "order": instance.pk},
        )


class ShopOrderPositionSerializer(OrderProductShopSerializer):
    """Serializer для модели ProductShopModel.
    Состоит на основе OrderProductShopSerializer только с другим количеством полей
    """

    class Meta(OrderProductShopSerializer.Meta):
        fields = ("product_id", "product_name", "description", "params")


class ShopOrderItemsSerializer(OrderPositionSerializer):
    """Serializer для ProductShopModel.
    Состоит на основе модели OrderPositionSerializer, но с переопределенным position и другим количеством полей"""

    position = ShopOrderPositionSerializer(read_only=True)

    class Meta(OrderPositionSerializer.Meta):
        fields = ("position", "quantity", "price", "price_rrc")
