from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction

import logging

logger = logging.getLogger(__name__)

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = SignupForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        try:
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

        except Exception:
            logger.exception("Signup failed")
            raise

    return render(request, "accounts/signup.html", {"form": form})
