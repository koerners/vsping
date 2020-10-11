import urllib.request
from datetime import datetime

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.shortcuts import render
from django.urls import reverse

from sitechecker.forms import CustomUserCreationForm, JobForm
from sitechecker.models import Job
from sitechecker.src.controller import get_screenshot


@login_required
def dashboard(request):

    context = {
        'userjobs': Job.objects.filter(owner=request.user)
    }

    return render(request, "dashboard.html", context)

def landing(request):
    return render(request, "landing.html")




@login_required
def job_detail(request, job_id):
    user_job = Job.objects.filter(owner=request.user, id=int(job_id))
    if len(user_job)<1:
        return redirect(reverse("dashboard"))

    context = {
        'userjob': user_job[0]
    }

    return render(request, "job_detail.html", context)

@login_required
def new_job(request):
    if request.method == "GET":

        return render(
            request, "new_job.html",
            {"form": JobForm}
        )

    elif request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.owner = request.user
            job.date_added = datetime.now()
            try:
                fp = urllib.request.urlopen(str(job.url))
                mybytes = fp.read()
                job.html_current = mybytes

            except:
                pass

            job.screenshot = get_screenshot(job.url)


            job.save()

            return redirect("job_detail", job_id=job.id)


def register(request):
    if request.method == "GET":

        return render(

            request, "register.html",

            {"form": CustomUserCreationForm}

        )

    elif request.method == "POST":

        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.backend = "django.contrib.auth.backends.ModelBackend"
            user.save()

            login(request, user)

            return redirect(reverse("dashboard"))
