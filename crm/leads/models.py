import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

from leads.validators import phone_regex


User = get_user_model()

LEAD_STATUS = (
    ("1", "Создана заявка"),
    ("2", "Купил"),
    ("3", "Отказ"),
)

LEAD_SOURCE = (
    ("", "----------"),
    ("Яндекс Директ", "Яндекс Директ"),
    ("Вконтакте", "Вконтакте"),
    ("Инстаграм", "Инстаграм"),
    ("SEO", "SEO"),
    ("Посоветовали", "Посоветовали"),
    ("Прочее", "Прочее"),
)


class Lead(models.Model):
    name = models.CharField(max_length=100)
    # phone_regex = RegexValidator(
    #     regex=r"^(\+7)(\d{10})$",
    #     message="Номер телефона должен быть введен в формате: '+79999999999'",
    # )
    phone_number = models.CharField(
        validators=[phone_regex], max_length=12, unique=True
    )
    date_of_creation = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=LEAD_STATUS, default="1")
    source = models.CharField(max_length=20, choices=LEAD_SOURCE)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-pk"]

    def get_absolute_url(self):
        return f"/leads/{self.pk}/"


class Task(models.Model):
    lead = models.ForeignKey(
        Lead, on_delete=models.CASCADE, related_name="tasks"
    )
    name = models.CharField(max_length=200)
    comment = models.TextField()
    task_date = models.DateField(default=timezone.now)
    active = models.BooleanField(default=True)
    date_of_creation = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["task_date"]


class Deal(models.Model):
    name = models.CharField(max_length=200)
    total = models.PositiveIntegerField()
    date_of_deal = models.DateTimeField(auto_now_add=True)
    lead = models.ForeignKey(
        Lead, on_delete=models.CASCADE, related_name="deals"
    )

    class Meta:
        ordering = ["-date_of_deal"]
