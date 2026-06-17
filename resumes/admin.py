from django.contrib import admin

from .models import Candidate, EmailLog


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "job", "score", "status", "uploaded_at")
    list_filter = ("status", "uploaded_at", "job")
    search_fields = ("name", "email", "skills", "raw_text")


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ("candidate", "recipient", "subject", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("recipient", "subject", "error_message")
