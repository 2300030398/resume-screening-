import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "resume_screening.settings")

app = Celery("resume_screening")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
