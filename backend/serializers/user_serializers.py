from django.core.validators import MinValueValidator
from rest_framework import serializers
from rest_framework.reverse import reverse

from backend.models import (
    OrderAddressModel,
    OrderItemsModel,
    OrderModel,
    ProductModel,
    ProductShopModel,
    ShopModel,
    UserModel,
)
from backend.serializers.product_serializers import ProductShopDetailListSerializer
from backend.utils.constants import ErrorMessages


class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddressModel
        fields = ("postal_code", "country", "region", "city")


class OrderItemsCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source="position.product", required=True)
    shop_id = serializers.IntegerField(source="position.shop", required=True)
    quantity = serializers.IntegerField(required=True, allow_null=False, validators=[MinValueValidator(1)])

    class Meta:
        model = OrderItemsModel
        fields = ("product_id", "shop_id", "quantity")

    @staticmethod
    def validate_product_id(value):
        product = ProductModel.objects.filter(pk=value)
        if not product.exists():
            raise serializers.ValidationError(ErrorMessages.PRODUCT_WITH_ID_NOT_FOUND)
        return value

    @staticmethod
    def validate_shop_id(value):
        shop = ShopModel.objects.filter(pk=value)
        if not shop.exists():
            raise serializers.ValidationError(ErrorMessages.SHOP_WITH_ID_NOT_FOUND)
        return value

    def validate(self, validated_data):
        position = validated_data.get("position")
        position = ProductShopModel.objects.filter(**position).first()
        if not position:
            raise serializers.ValidationError(ErrorMessages.POSITION_WITH_ID_NOT_FOUND)
        if position.quantity == 0:
            raise serializers.ValidationError(ErrorMessages.POSITION_IS_OUT_OF_STOCK)
        elif position.quantity < validated_data.get("quantity"):
            raise serializers.ValidationError(ErrorMessages.LESSER_QUANTITY)
        return validated_data


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display", read_only=True)
    details = serializers.HyperlinkedIdentityField(
        "order_detail", lookup_field="pk", lookup_url_kwarg="order", read_only=True
    )
    address = OrderAddressSerializer(write_only=True)
    order_items = OrderItemsCreateSerializer(many=True, allow_null=False, allow_empty=False, write_only=True)

    class Meta:
        model = OrderModel
        fields = ("id", "address", "created_at", "status", "order_items", "additional", "details")
        extra_kwargs = {"additional": {"write_only": True}, "id": {"read_only": True}}

    def create(self, validated_data):
        user = self.context["request"].user
        address, _ = OrderAddressModel.objects.get_or_create(**validated_data.get("address"))
        order = self.Meta.model.objects.create(user=user, address=address, additional=validated_data.get("additional"))
        order_items = validated_data.get("order_items")
        for item in order_items:
            position = ProductShopModel.objects.get(**item.get("position"))
            OrderItemsModel.objects.create(order=order, position=position, quantity=item.get("quantity"))
        return order


class OrderProductShopSerializer(ProductShopDetailListSerializer):
    class Meta(ProductShopDetailListSerializer.Meta):
        fields = ("product_id", "product_name", "shop_id", "shop_name", "description", "params")


class OrderPositionSerializer(serializers.ModelSerializer):
    position = OrderProductShopSerializer(read_only=True)
    sum = serializers.SerializerMethodField("get_sum", read_only=True)

    class Meta:
        model = OrderItemsModel
        fields = ("position", "quantity", "price", "price_rrc", "sum")

    @staticmethod
    def get_sum(instance: OrderItemsModel):
        return instance.get_sum_price()


class OrderDetailSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display", read_only=True)
    address = OrderAddressSerializer(read_only=True)
    items = serializers.HyperlinkedIdentityField("order_positions", lookup_field="pk", lookup_url_kwarg="order")
    total_price = serializers.SerializerMethodField("get_total_price", read_only=True)

    class Meta:
        model = OrderModel
        fields = ("id", "created_at", "status", "address", "additional", "items", "total_price")

    @staticmethod
    def get_total_price(instance: OrderModel):
        return instance.get_total_price()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    orders = serializers.SerializerMethodField("get_orders_link", read_only=True)

    class Meta:
        model = UserModel
        fields = ("username", "email", "password", "orders")
        extra_kwargs = {"password": {"write_only": True}}

    @staticmethod
    def validate_email(value: str):
        if UserModel.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(ErrorMessages.USER_EMAIL_IS_EXIST)
        return value

    def create(self, validated_data):
        return UserModel.objects.create_user(**validated_data)

    def get_orders_link(self, instance: UserModel):
        return reverse("orders", request=self.context["request"])
