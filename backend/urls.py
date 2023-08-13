from django.urls import path

from backend.views.shop_views import ShopDetailView, ShopListView, ShopPriceListView, ShopUpdateStatusView
from backend.views.user_views import UserProfileView, UserRegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # user
    path("users/profile/", UserProfileView.as_view(), name="profile"),
    path("users/register/", UserRegisterView.as_view(), name="register"),
    path("users/token/", TokenObtainPairView.as_view(), name="token"),
    path("users/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # shop
    path("shops/", ShopListView.as_view(), name="shops"),
    path("shops/<slug>/", ShopDetailView.as_view(), name="shop_detail"),
    path("shops/<slug>/products/", ShopPriceListView.as_view(), name="shop_price_list"),
    path("shops/<slug>/status/", ShopUpdateStatusView.as_view(), name="shop_update_status"),
]
