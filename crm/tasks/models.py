from django.db import models
from django.contrib.auth import get_user_model
from leads.models import Lead


User = get_user_model()


class Task(models.Model):
    lead = models.ForeignKey(
        Lead, on_delete=models.CASCADE, related_name="tasks"
    )
    comment = models.TextField()
    task_date = models.DateField()
