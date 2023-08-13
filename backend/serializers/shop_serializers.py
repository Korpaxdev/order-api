from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpRequest
from rest_framework import serializers

from backend.models import SHOP_STATUS_CHOICES, ProductShopModel, ShopModel
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
    id = serializers.IntegerField(read_only=True, source="product.pk")
    name = serializers.CharField(read_only=True, source="product.name")
    categories = serializers.SerializerMethodField(read_only=True, method_name="get_categories_name")
    params = ProductParameterSerializer(many=True, source="product_parameters")

    class Meta:
        model = ProductShopModel
        fields = ("id", "name", "categories", "description", "quantity", "price", "price_rrc", "params")

    @staticmethod
    def get_categories_name(instance: ProductShopModel):
        return [cat.name for cat in instance.product.categories.all()]


class ShopUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopModel
        fields = ("status",)

    def validate_status(self, value):
        if value and not self.instance.price_file:
            status_name = dict(SHOP_STATUS_CHOICES).get(value)
            raise serializers.ValidationError(
                f"Невозможно установить статус {status_name}, когда у магазина отсутствует прайс файл"
            )
        return value


class ShopPriceFileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopModel
        fields = ("price_file",)
        extra_kwargs = {"price_file": {"required": True, "allow_null": False}}

    def validate_price_file(self, value: InMemoryUploadedFile):
        instance: ShopModel = self.instance
        if not instance.is_valid_price_file(value):
            formats_string = ",".join(settings.PRICE_FILE_FORMATS)
            raise serializers.ValidationError(f"Недопустимый формат файла. Допустимые форматы: {formats_string}")
        return value
