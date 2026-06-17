import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("resumes", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmailLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("recipient", models.EmailField(blank=True, max_length=254)),
                ("subject", models.CharField(blank=True, max_length=255)),
                ("status", models.CharField(choices=[("sent", "Sent"), ("failed", "Failed"), ("skipped", "Skipped")], max_length=20)),
                ("error_message", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("candidate", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="email_logs", to="resumes.candidate")),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
