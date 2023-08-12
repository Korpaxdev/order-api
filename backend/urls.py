from django.urls import path

from backend.views.hello_view import HelloView

urlpatterns = [
    path('', HelloView.as_view())
]
