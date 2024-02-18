from django import forms

from .models import Lead, Task


class DateInput(forms.DateInput):
    input_type = "date"


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
            "task_date": DateInput(),
        }
