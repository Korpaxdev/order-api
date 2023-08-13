from django.http import HttpRequest
from rest_framework import serializers

from backend.models import ShopModel


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
