from rest_framework import serializers

from backend.models import ProductParameterModel


class ProductParameterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True, source="param.name")

    class Meta:
        model = ProductParameterModel
        fields = ("name", "value")
