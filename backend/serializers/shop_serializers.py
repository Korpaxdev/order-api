from django.http import HttpRequest
from rest_framework import serializers

from backend.models import ProductShopModel, ShopModel
from backend.serializers.product_serializers import ProductParameterSerializer


class ShopListSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display")
    detail = serializers.HyperlinkedIdentityField("shop_detail", lookup_field="slug")

    class Meta:
        model = ShopModel
        fields = ("id", "name", "status", "detail")


class ShopDetailSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display")
    price_list = serializers.HyperlinkedIdentityField("shop_price_list", lookup_field="slug")

    def __init__(self, instance: ShopModel, **kwargs):
        # Проверяется если пользователь админ или менеджер то поле price_file остается, если же нет то удаляется
        context = kwargs["context"]
        request: HttpRequest = context["request"]
        if not instance.status:
            del self.fields["price_list"]
        if not instance.is_manager_or_admin(request.user):
            del self.fields["price_file"]
        super().__init__(instance, **kwargs)

    class Meta:
        model = ShopModel
        fields = ("id", "name", "email", "phone", "status", "price_list", "price_file")


class ShopPriceListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True, source="product.name")
    categories = serializers.SerializerMethodField(read_only=True, method_name="get_categories_name")
    params = ProductParameterSerializer(many=True, source="product_parameters")

    class Meta:
        model = ProductShopModel
        fields = ("name", "categories", "description", "quantity", "price", "price_rrc", "params")

    @staticmethod
    def get_categories_name(instance: ProductShopModel):
        return [cat.name for cat in instance.product.categories.all()]
