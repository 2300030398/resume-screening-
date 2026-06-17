from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        RECRUITER = "recruiter", "Recruiter"
        ADMIN = "admin", "Admin"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.RECRUITER)
    company_name = models.CharField(max_length=120, blank=True)

    @property
    def is_recruiter(self):
        return self.role == self.Role.RECRUITER
