from django import forms

from .models import Lead, Task


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ("name", "phone_number")
        labels = {
            "name": "Имя",
            "phone_number": "Телефон",
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("comment", "task_date")
        labels = {
            "comment": "Комментарий",
            "task_date": "Дата задачи",
        }
