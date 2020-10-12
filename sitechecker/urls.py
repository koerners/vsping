from django.conf.urls import url
from django.urls import include, path

from sitechecker.src.controller import check_jobs
from sitechecker.views import dashboard, register, new_job, job_detail, landing, job_edit, job_reset, job_delete

check_jobs(repeat=900)
urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^register/", register, name="register"),
    url(r"^oauth/", include("social_django.urls")),
    path("", landing, name="landing"),
    path("jobs/new/", new_job, name="new_job"),
    path('jobs/edit/<int:job_id>/', job_edit, name="job_edit"),
    path('jobs/reset/<int:job_id>/', job_reset, name="job_reset"),
    path('jobs/delete/<int:job_id>/', job_delete, name="job_delete"),
    path('jobs/<int:job_id>/', job_detail, name="job_detail"),
    path("jobs/", dashboard, name="dashboard"),

]
