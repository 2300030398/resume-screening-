from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import RecruiterRegistrationForm


def register(request):
    if request.method == "POST":
        form = RecruiterRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard:home")
    else:
        form = RecruiterRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})
