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
# Add this to the bottom of your existing accounts/views.py

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import User


def is_admin(user):
    return user.is_staff or user.role == User.Role.ADMIN


@login_required
@user_passes_test(is_admin)
def admin_overview(request):
    from recruiter.models import JobOpening
    from resumes.models import Candidate, EmailLog

    recruiters = User.objects.all().order_by('-date_joined')

    # Activity summary per recruiter
    recruiter_data = []
    for r in recruiters:
        jobs_count = JobOpening.objects.filter(recruiter=r).count()
        candidates_count = Candidate.objects.filter(job__recruiter=r).count()
        recruiter_data.append({
            "user": r,
            "jobs_count": jobs_count,
            "candidates_count": candidates_count,
            "last_login": r.last_login,
        })

    # Platform-wide stats
    total_recruiters = recruiters.count()
    active_today = recruiters.filter(last_login__date=timezone.now().date()).count()
    active_week = recruiters.filter(last_login__gte=timezone.now() - timedelta(days=7)).count()
    never_logged_in = recruiters.filter(last_login__isnull=True).count()

    total_jobs = JobOpening.objects.count()
    total_candidates = Candidate.objects.count()
    total_emails_sent = EmailLog.objects.filter(status=EmailLog.Status.SENT).count()

    context = {
        "recruiter_data": recruiter_data,
        "total_recruiters": total_recruiters,
        "active_today": active_today,
        "active_week": active_week,
        "never_logged_in": never_logged_in,
        "total_jobs": total_jobs,
        "total_candidates": total_candidates,
        "total_emails_sent": total_emails_sent,
    }
    return render(request, "accounts/admin_overview.html", context)