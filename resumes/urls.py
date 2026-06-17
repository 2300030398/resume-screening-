from django.urls import path

from . import views

app_name = "resumes"

urlpatterns = [
    path("upload/", views.resume_upload, name="resume_upload"),
    path("candidates/", views.candidate_list, name="candidate_list"),
    path("candidates/<int:pk>/", views.candidate_detail, name="candidate_detail"),
    path("candidates/<int:pk>/status/", views.candidate_status_update, name="candidate_status_update"),
    path("email-logs/", views.email_log_list, name="email_log_list"),
    path("export/csv/", views.export_candidates_csv, name="export_csv"),
    path("export/excel/", views.export_candidates_excel, name="export_excel"),
]