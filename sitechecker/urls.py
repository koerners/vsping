
from django.conf.urls import url
from django.urls import include

from sitechecker.views import dashboard, register

urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^register/", register, name="register"),
    url(r"^dashboard/", dashboard, name="dashboard"),
    url(r"^oauth/", include("social_django.urls")),
]
