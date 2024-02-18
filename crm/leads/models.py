from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

User = get_user_model()


class Lead(models.Model):
    name = models.CharField(max_length=100)
    phone_regex = RegexValidator(
        regex=r"^(\+7)(\d{10})$",
        message="Номер телефона должен быть введен в формате: '+79999999999'",
    )
    phone_number = models.CharField(
        validators=[phone_regex], max_length=12, unique=True
    )
    date_of_creation = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return f"/leads/{self.pk}/"


class Task(models.Model):
    lead = models.ForeignKey(
        Lead, on_delete=models.CASCADE, related_name="tasks"
    )
    name = models.CharField(max_length=200)
    comment = models.TextField()
    task_date = models.DateField()
