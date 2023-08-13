from django.http import HttpRequest
from rest_framework import permissions
from rest_framework.views import APIView

from backend.models import ShopModel


class IsManagerOrAdminPermission(permissions.BasePermission):
    def has_object_permission(self, request: HttpRequest, view: APIView, instance: ShopModel):
        return instance.is_manager_or_admin(request.user)
