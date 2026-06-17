from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import JobOpeningForm
from .models import JobOpening


@login_required
def job_list(request):
    jobs = JobOpening.objects.filter(recruiter=request.user)
    return render(request, "recruiter/job_list.html", {"jobs": jobs})


@login_required
def job_detail(request, pk):
    job = get_object_or_404(JobOpening, pk=pk, recruiter=request.user)
    candidates = job.candidates.order_by("-score", "status")
    return render(request, "recruiter/job_detail.html", {"job": job, "candidates": candidates})


@login_required
def job_create(request):
    form = JobOpeningForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        job = form.save(commit=False)
        job.recruiter = request.user
        job.save()
        return redirect(job)
    return render(request, "recruiter/job_form.html", {"form": form, "title": "Create Job"})


@login_required
def job_update(request, pk):
    job = get_object_or_404(JobOpening, pk=pk, recruiter=request.user)
    form = JobOpeningForm(request.POST or None, instance=job)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(job)
    return render(request, "recruiter/job_form.html", {"form": form, "title": "Edit Job"})


@login_required
def job_delete(request, pk):
    job = get_object_or_404(JobOpening, pk=pk, recruiter=request.user)
    if request.method == "POST":
        job.delete()
        return redirect("recruiter:job_list")
    return render(request, "recruiter/job_confirm_delete.html", {"job": job})
