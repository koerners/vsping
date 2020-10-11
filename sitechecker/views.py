from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.shortcuts import render
from django.urls import reverse

from sitechecker.forms import CustomUserCreationForm

@login_required
def dashboard(request):
    return render(request, "dashboard.html")


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
