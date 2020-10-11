
from django.conf.urls import url
from django.urls import include, path

from sitechecker.views import dashboard, register, new_job, job_detail

urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^register/", register, name="register"),
    url(r"^oauth/", include("social_django.urls")),

    path("jobs/new/", new_job, name="new_job"),
    path('jobs/<int:job_id>/', job_detail, name="job_detail"),
    path("jobs/", dashboard, name="dashboard"),

]
