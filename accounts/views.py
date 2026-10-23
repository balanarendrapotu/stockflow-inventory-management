from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction

from .forms import SignupForm
from .models import Organization


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = SignupForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            user = User.objects.create_user(
                username=form.cleaned_data["email"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            Organization.objects.create(
                name=form.cleaned_data["organization_name"],
                owner=user,
            )

        login(request, user)
        return redirect("dashboard")

    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        user = authenticate(
            request, username=email, password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        messages.error(request, "Invalid email or password.")

    return render(request, "accounts/login.html")


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return redirect("dashboard")