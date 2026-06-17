from django.contrib import admin

from .models import JobOpening


@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ("title", "recruiter", "minimum_experience", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "required_skills", "description")
