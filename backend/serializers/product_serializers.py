from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from backend.models import ProductModel, ProductParameterModel, ProductShopModel
from backend.utils.product_utils import get_cats_names


class ProductParameterSerializer(serializers.ModelSerializer):
    """Serializer для модели ProductParameterModel"""

    name = serializers.CharField(read_only=True, source="param.name")

    class Meta:
        model = ProductParameterModel
        fields = ("name", "value")


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer для списка из модели ProductModel"""

    categories = serializers.SerializerMethodField("get_categories")
    details = serializers.HyperlinkedIdentityField(
        "product_details_list", lookup_field="slug", lookup_url_kwarg="product"
    )

    class Meta:
        model = ProductModel
        fields = ("id", "name", "categories", "details")

    @staticmethod
    @extend_schema_field(serializers.ListField)
    def get_categories(instance: ProductModel):
        return get_cats_names(instance)


class ProductShopDetailListSerializer(serializers.ModelSerializer):
    """Serializer для списка из модели ProductShopModel"""

    product_id = serializers.IntegerField(read_only=True, source="product.pk")
    product_name = serializers.CharField(read_only=True, source="product.name")
    shop_id = serializers.IntegerField(read_only=True, source="shop.pk")
    shop_name = serializers.CharField(read_only=True, source="shop.name")
    params = ProductParameterSerializer(many=True, read_only=True, source="product_parameters")
    categories = serializers.SerializerMethodField("get_categories")

    class Meta:
        model = ProductShopModel
        fields = (
            "product_id",
            "product_name",
            "categories",
            "shop_id",
            "shop_name",
            "description",
            "params",
            "quantity",
            "price",
            "price_rrc",
        )

    @staticmethod
    @extend_schema_field(serializers.ListField)
    def get_categories(instance: ProductShopModel):
        return get_cats_names(instance.product)
