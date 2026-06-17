from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RecruiterRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", "email", "company_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.RECRUITER
        if commit:
            user.save()
        return user
