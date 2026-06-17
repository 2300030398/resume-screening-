from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Recruiter Details", {"fields": ("role", "company_name")}),)
    list_display = ("username", "email", "role", "company_name", "is_staff")
