from rest_framework import serializers

from backend.models import UserModel


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = UserModel
        fields = ("username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    @staticmethod
    def validate_email(value: str):
        if UserModel.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Такой email уже используется")
        return value

    def create(self, validated_data):
        return UserModel.objects.create_user(**validated_data)
