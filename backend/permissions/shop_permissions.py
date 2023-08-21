from rest_framework import permissions

from backend.models import ShopModel, UserModel


class IsManagerOrAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user: UserModel = request.user
        shop = ShopModel.objects.filter(slug=view.kwargs.get("shop")).first()
        return user.is_superuser or user.is_manager(shop)
