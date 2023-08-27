from collections import defaultdict

from django.core.validators import MinValueValidator
from django.utils.datetime_safe import datetime
from rest_framework import serializers
from rest_framework.reverse import reverse

from backend.models import (
    OrderAddressModel,
    OrderItemsModel,
    OrderModel,
    PasswordResetTokenModel,
    ProductModel,
    ProductShopModel,
    ShopModel,
    UserModel,
)
from backend.serializers.product_serializers import ProductShopDetailListSerializer
from backend.tasks.email_tasks import send_new_order_email
from backend.utils.constants import ErrorMessages
from backend.utils.validation import password_validation


class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddressModel
        fields = ("postal_code", "country", "region", "city")


class OrderItemsCreateSerializer(serializers.ModelSerializer):
    product = serializers.IntegerField(source="position.product")
    shop = serializers.IntegerField(source="position.shop")
    quantity = serializers.IntegerField(required=True, allow_null=False, validators=[MinValueValidator(1)])

    class Meta:
        model = OrderItemsModel
        fields = ("product", "shop", "quantity")

    @staticmethod
    def validate_product(value):
        product = ProductModel.objects.filter(pk=value).first()
        if not product:
            raise serializers.ValidationError(ErrorMessages.PRODUCT_WITH_ID_NOT_FOUND)
        return value

    @staticmethod
    def validate_shop(value):
        shop: ShopModel | None = ShopModel.objects.filter(pk=value).first()
        if not shop:
            raise serializers.ValidationError(ErrorMessages.SHOP_WITH_ID_NOT_FOUND)
        if not shop.status:
            raise serializers.ValidationError(ErrorMessages.SHOP_DOESNT_ACCEPT_ORDERS)
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
        address = validated_data.get("address")
        address, _ = OrderAddressModel.objects.get_or_create(
            postal_code=address.get("postal_code"),
            country__iexact=address.get("country"),
            region__iexact=address.get("region"),
            city__iexact=address.get("city"),
            defaults=address,
        )
        order = self.Meta.model.objects.create(user=user, address=address, additional=validated_data.get("additional"))
        order_items = validated_data.get("order_items")
        for order_item in order_items:
            order_item_quantity = order_item.get("quantity")
            position = ProductShopModel.objects.get(**order_item.get("position"))
            OrderItemsModel.objects.create(order=order, position=position, quantity=order_item_quantity)
        send_new_order_email.delay(order.pk)
        return order

    @staticmethod
    def validate_order_items(validated_data):
        duplicates = defaultdict(list)
        for data in validated_data:
            position = data["position"]
            if position in duplicates["position"]:
                raise serializers.ValidationError(ErrorMessages.PRODUCT_SHOP_UNIQUE_TOGETHER)
            else:
                duplicates["position"].append(position)
        return validated_data


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
    password = serializers.CharField(validators=[password_validation], write_only=True, required=True)
    email = serializers.EmailField(required=True)
    orders = serializers.SerializerMethodField("get_orders_link", read_only=True)

    class Meta:
        model = UserModel
        fields = ("pk", "username", "email", "password", "orders")

    @staticmethod
    def validate_email(value: str):
        if UserModel.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(ErrorMessages.USER_EMAIL_IS_EXIST)
        return value

    def create(self, validated_data):
        return UserModel.objects.create_user(**validated_data)

    def get_orders_link(self, instance: UserModel):
        return reverse("orders", request=self.context["request"])


class UserPasswordResetTokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, write_only=True)

    class Meta:
        model = PasswordResetTokenModel
        fields = ("email",)

    @staticmethod
    def validate_email(value: str):
        user = UserModel.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError(ErrorMessages.USER_WITH_EMAIL_NOT_FOUND)
        token = PasswordResetTokenModel.objects.filter(user__email=value, expire__gt=datetime.now()).first()
        if token:
            raise serializers.ValidationError(ErrorMessages.RESET_PASSWORD_EMAIL_ALREADY_SENT)
        return value

    def create(self, validated_data):
        email = validated_data.get("email")
        user = UserModel.objects.get(email=email)
        instance = PasswordResetTokenModel.objects.create(user=user)
        return instance


class UserUpdatePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[password_validation], write_only=True, required=True)

    class Meta:
        model = UserModel
        fields = ("id", "username", "email", "password")
        read_only_fields = ("id", "username", "email")

    def update(self, instance: UserModel, validated_data):
        instance.set_password(validated_data.get("password"))
        instance.save()
        return instance
