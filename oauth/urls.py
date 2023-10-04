from django.conf import settings
from django.urls import path
from social_core.utils import setting_name
from social_django.views import complete

from oauth.views import AuthByAccessTokenView

extra = getattr(settings, setting_name("TRAILING_SLASH"), True) and "/" or ""

app_name = "social"


urlpatterns = [
    path(f"complete/<str:backend>{extra}", complete, name="complete"),
    path(f"login/<str:backend>/", AuthByAccessTokenView.as_view(), name="login"),
]
