from django.urls import path

from backend.views.user_views import UserProfileView, UserRegisterView

urlpatterns = [
    path("users/profile/", UserProfileView.as_view(), name="profile"),
    path("users/register/", UserRegisterView.as_view(), name="register"),
]
