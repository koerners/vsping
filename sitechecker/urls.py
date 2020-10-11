from django.conf.urls import url
from django.urls import include, path

from sitechecker.views import dashboard, register, new_job, job_detail, landing, job_edit

urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^register/", register, name="register"),
    url(r"^oauth/", include("social_django.urls")),
    path("", landing, name="landing"),
    path("jobs/new/", new_job, name="new_job"),
    path('jobs/edit/<int:job_id>/', job_edit, name="job_edit"),
    path('jobs/<int:job_id>/', job_detail, name="job_detail"),
    path("jobs/", dashboard, name="dashboard"),

]
