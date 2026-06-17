from django.db import models
from django.urls import reverse

from recruiter.models import JobOpening


class Candidate(models.Model):
    class Status(models.TextChoices):
        REVIEW = "review", "Review"
        SHORTLISTED = "shortlisted", "Shortlisted"
        REJECTED = "rejected", "Rejected"

    job = models.ForeignKey(JobOpening, on_delete=models.CASCADE, related_name="candidates")
    resume = models.FileField(upload_to="resumes/%Y/%m/%d/")
    name = models.CharField(max_length=160, blank=True)
    email = models.EmailField(blank=True)
    skills = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    raw_text = models.TextField(blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REVIEW)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-score", "-uploaded_at"]

    def __str__(self):
        return self.name or self.resume.name

    def skill_list(self):
        return [skill.strip().lower() for skill in self.skills.split(",") if skill.strip()]

    def get_absolute_url(self):
        return reverse("resumes:candidate_detail", args=[self.pk])


class EmailLog(models.Model):
    class Status(models.TextChoices):
        SENT = "sent", "Sent"
        FAILED = "failed", "Failed"
        SKIPPED = "skipped", "Skipped"

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="email_logs")
    recipient = models.EmailField(blank=True)
    subject = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_status_display()} email to {self.recipient or 'unknown'}"
