import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("recruiter", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Candidate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("resume", models.FileField(upload_to="resumes/%Y/%m/%d/")),
                ("name", models.CharField(blank=True, max_length=160)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("skills", models.TextField(blank=True)),
                ("experience_years", models.PositiveIntegerField(default=0)),
                ("raw_text", models.TextField(blank=True)),
                ("score", models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ("status", models.CharField(choices=[("review", "Review"), ("shortlisted", "Shortlisted"), ("rejected", "Rejected")], default="review", max_length=20)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("processed_at", models.DateTimeField(blank=True, null=True)),
                ("job", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="candidates", to="recruiter.jobopening")),
            ],
            options={"ordering": ["-score", "-uploaded_at"]},
        ),
    ]
