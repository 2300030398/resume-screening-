from django import forms

from .models import JobOpening


class JobOpeningForm(forms.ModelForm):
    class Meta:
        model = JobOpening
        fields = ("title", "description", "required_skills", "minimum_experience", "shortlist_message", "is_active")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
            "required_skills": forms.TextInput(attrs={"placeholder": "Python, Django, PostgreSQL"}),
            "shortlist_message": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "e.g. We were impressed by your project experience and would love to move forward with your application.",
            }),
        }