from rest_framework import serializers
from rest_framework.reverse import reverse

from backend.models import OrderAddressModel, OrderModel, OrderPositionModel, UserModel
from backend.serializers.product_serializers import ProductShopDetailListSerializer


class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddressModel
        fields = ('postal_code', 'country', 'region', 'city')


class OrderListSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display")
    details = serializers.HyperlinkedIdentityField("order_detail")

    class Meta:
        model = OrderModel
        fields = ('id', 'created_at', 'status', 'details')


class OrderPositionProductSerializer(ProductShopDetailListSerializer):
    class Meta(ProductShopDetailListSerializer.Meta):
        fields = (
            "product_id",
            "product_name",
            "categories",
            "shop_id",
            "shop_name",
            "description",
            "params",
        )


class OrderPositionSerializer(serializers.ModelSerializer):
    position = OrderPositionProductSerializer()
    sum = serializers.SerializerMethodField('get_sum')

    class Meta:
        model = OrderPositionModel
        fields = ('position', 'quantity', 'price', 'price_rrc', 'sum')

    @staticmethod
    def get_sum(instance: OrderPositionModel):
        return instance.get_sum_price()


class OrderDetailSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display")
    address = OrderAddressSerializer()
    positions = serializers.SerializerMethodField('get_positions_link')
    total_price = serializers.SerializerMethodField('get_total_price')

    class Meta:
        model = OrderModel
        fields = ('id', 'created_at', 'status', 'address', 'positions', 'total_price')

    def get_positions_link(self, instance: OrderModel):
        return reverse('order_positions', request=self.context['request'], kwargs={'pk': instance.pk})

    @staticmethod
    def get_total_price(instance: OrderModel):
        return sum([position.get_sum_price() for position in instance.positions.all()])


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
            raise serializers.ValidationError("Такой email уже используется")
        return value

    def create(self, validated_data):
        return UserModel.objects.create_user(**validated_data)

    def get_orders_link(self, instance: UserModel):
        return reverse('orders', request=self.context['request'])
