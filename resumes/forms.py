from django import forms
from .models import Candidate


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class ResumeUploadForm(forms.Form):
    job = forms.ModelChoiceField(queryset=None)
    resumes = MultipleFileField(
        label="Upload Resumes",
        help_text="You can select multiple PDF/DOC files at once.",
    )

    def __init__(self, *args, recruiter=None, **kwargs):
        super().__init__(*args, **kwargs)
        if recruiter is not None:
            from recruiter.models import JobOpening
            self.fields["job"].queryset = JobOpening.objects.filter(
                recruiter=recruiter, is_active=True
            )


class CandidateStatusForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ("status",)