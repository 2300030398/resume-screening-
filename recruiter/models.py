from django.conf import settings
from django.db import models
from django.urls import reverse


class JobOpening(models.Model):
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=160)
    description = models.TextField()
    required_skills = models.TextField(help_text="Comma-separated skills such as Python, Django, SQL")
    minimum_experience = models.PositiveIntegerField(default=0, help_text="Minimum years of experience")
    shortlist_message = models.TextField(
        blank=True,
        help_text="Custom message for the shortlist email body. Leave blank to use the default message.",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def skill_list(self):
        return [skill.strip().lower() for skill in self.required_skills.split(",") if skill.strip()]

    def get_absolute_url(self):
        return reverse("recruiter:job_detail", args=[self.pk])