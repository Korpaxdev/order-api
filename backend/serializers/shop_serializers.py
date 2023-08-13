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

    class Meta:
        model = ShopModel
        fields = ("id", "name", "email", "phone", "status")
