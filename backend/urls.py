from django.urls import path

from backend.views.shop_views import ShopDetailView, ShopListView, ShopPriceListView
from backend.views.user_views import UserProfileView, UserRegisterView

urlpatterns = [
    # user
    path("users/profile/", UserProfileView.as_view(), name="profile"),
    path("users/register/", UserRegisterView.as_view(), name="register"),
    # shop
    path("shops/", ShopListView.as_view(), name="shops"),
    path("shops/<slug>/", ShopDetailView.as_view(), name="shop_detail"),
    path("shops/<slug>/products/", ShopPriceListView.as_view(), name="shop_price_list"),
]
