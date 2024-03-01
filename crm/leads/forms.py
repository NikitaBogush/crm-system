from django import forms

from .models import Lead, Task, Deal


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ("name", "phone_number", "status")
        labels = {
            "name": "Имя",
            "phone_number": "Телефон",
            "status": "Статус",
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


class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ("name", "total")
        labels = {
            "name": "Наименование сделки",
            "total": "Сумма сделки",
        }
