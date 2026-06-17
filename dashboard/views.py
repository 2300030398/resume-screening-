from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.shortcuts import render

from resumes.models import Candidate
from recruiter.models import JobOpening


@login_required
def home(request):
    candidates = Candidate.objects.filter(job__recruiter=request.user)
    stats = candidates.aggregate(total=Count("id"), average_score=Avg("score"))

    score_0_25   = candidates.filter(score__lt=25).count()
    score_25_50  = candidates.filter(score__gte=25, score__lt=50).count()
    score_50_75  = candidates.filter(score__gte=50, score__lt=75).count()
    score_75_100 = candidates.filter(score__gte=75).count()

    jobs = JobOpening.objects.filter(recruiter=request.user, is_active=True).annotate(
        total=Count("candidates"),
        shortlisted=Count("candidates", filter=Q(candidates__status=Candidate.Status.SHORTLISTED)),
        rejected=Count("candidates", filter=Q(candidates__status=Candidate.Status.REJECTED)),
        avg_score=Avg("candidates__score"),
    ).order_by("-created_at")[:6]

    context = {
        "total_resumes":  stats["total"] or 0,
        "average_score":  round(stats["average_score"] or 0, 1),
        "shortlisted":    candidates.filter(status=Candidate.Status.SHORTLISTED).count(),
        "rejected":       candidates.filter(status=Candidate.Status.REJECTED).count(),
        "review":         candidates.filter(status=Candidate.Status.REVIEW).count(),
        "top_candidates": candidates.select_related("job").order_by("-score")[:8],
        "jobs":           jobs,
        "score_buckets":  [score_0_25, score_25_50, score_50_75, score_75_100],
    }
    return render(request, "dashboard/home.html", context)