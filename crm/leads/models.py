from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

User = get_user_model()
# Статус лида:
LEAD_STATUS = (
    ("1", "Создана заявка"),
    ("2", "Купил"),
    ("3", "Отказ"),
)
# Источник лида:
LEAD_SOURCE = (
    ("", "----------"),
    ("Яндекс Директ", "Яндекс Директ"),
    ("Вконтакте", "Вконтакте"),
    ("Инстаграм", "Инстаграм"),
    ("SEO", "SEO"),
    ("Посоветовали", "Посоветовали"),
    ("Прочее", "Прочее"),
)
# Валидатор для проверки корректности номера телефона:
phone_regex = RegexValidator(
    regex=r"^(\+7)(\d{10})$",
    message="Номер телефона должен быть введен в формате: '+79999999999'",
)


class Lead(models.Model):
    # Имя лида:
    name = models.CharField(max_length=100)
    # Телефон:
    phone_number = models.CharField(
        validators=[phone_regex], max_length=12, unique=True
    )
    # Дата создания:
    date_of_creation = models.DateTimeField(auto_now_add=True)
    # Статус:
    status = models.CharField(max_length=1, choices=LEAD_STATUS, default="1")
    # Источник:
    source = models.CharField(max_length=20, choices=LEAD_SOURCE)
    # Комментарий:
    comment = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-pk"]

    def get_absolute_url(self):
        return f"/leads/{self.pk}/"


class Task(models.Model):
    lead = models.ForeignKey(
        Lead, on_delete=models.CASCADE, related_name="tasks"
    )
    # Название задачи:
    name = models.CharField(max_length=200)
    # Комментарий к задаче:
    comment = models.TextField()
    # Дата задачи:
    task_date = models.DateField(default=timezone.now)
    # Активна ли задача:
    active = models.BooleanField(default=True)
    # Дата создания задачи:
    date_of_creation = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["task_date"]


class Deal(models.Model):
    # Название сделки:
    name = models.CharField(max_length=200)
    # Сумма сделки:
    total = models.PositiveIntegerField()
    # Дата сделки:
    date_of_deal = models.DateTimeField(auto_now_add=True)
    lead = models.ForeignKey(
        Lead, on_delete=models.CASCADE, related_name="deals"
    )

    class Meta:
        ordering = ["-date_of_deal"]
