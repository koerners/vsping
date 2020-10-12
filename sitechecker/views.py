import logging

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from sitechecker.forms import CustomUserCreationForm, JobForm, UpdateJobForm
from sitechecker.models import Job
from sitechecker.src.controller import get_screenshot, get_html

logger = logging.getLogger(__name__)

@login_required
def dashboard(request):
    context = {
        'userjobs': Job.objects.filter(owner=request.user).order_by('-id')
    }

    return render(request, "dashboard.html", context)


def landing(request):
    return render(request, "landing.html")


@login_required
def job_detail(request, job_id):
    user_job = Job.objects.filter(owner=request.user, id=int(job_id))
    if len(user_job) < 1:
        return redirect(reverse("dashboard"))

    context = {
        'userjob': user_job[0]
    }

    return render(request, "job_detail.html", context)


@login_required
def job_edit(request, job_id):
    user_job = Job.objects.filter(owner=request.user, id=int(job_id))
    if len(user_job) < 1:
        return redirect(reverse("dashboard"))

    user_job = user_job[0]

    if request.method == 'POST':
        form = UpdateJobForm(instance=user_job, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("job_detail", job_id=user_job.id)

    else:
        form = UpdateJobForm(instance=user_job)

    return render(request, 'edit_job.html', {'form': form})


@login_required
def job_reset(request, job_id):
    user_job = Job.objects.filter(owner=request.user, id=int(job_id))
    if len(user_job) < 1:
        return redirect(reverse("dashboard"))

    user_job = user_job[0]
    user_job.similarity = 1
    user_job.is_active = True
    user_job.html_current = get_html(str(user_job.url))
    user_job.screenshot = get_screenshot(user_job.url)
    user_job.save()

    return redirect("job_detail", job_id=user_job.id)


@login_required
def job_delete(request, job_id):
    user_job = Job.objects.filter(owner=request.user, id=int(job_id))
    if len(user_job) < 1:
        return redirect(reverse("dashboard"))

    user_job = user_job[0]
    user_job.delete()

    return redirect(reverse("dashboard"))


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
            job.date_added = timezone.now()
            job.last_checked = timezone.now()
            job.last_change = timezone.now()

            try:
                job.html_current = get_html(str(job.url))
                job.screenshot = get_screenshot(job.url)
                logger.info('New Job created' + str(request.POST))

            except:
                logger.error('Something went wrong when creating a new Job! ' + str(request.POST))

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
