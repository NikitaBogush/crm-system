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
        fields = ("name", "comment", "task_date")
        labels = {
            "name": "Задача",
            "comment": "Комментарий",
            "task_date": "Дата задачи",
        }
        widgets = {
            "task_date": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={
                    "type": "date",
                },
            ),
        }
