from django.urls import include, path

urlpatterns = [path("", include("social_django.urls", namespace="social"))]
