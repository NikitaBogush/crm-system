from django import forms

from .models import Lead, Task, Deal, LEAD_SOURCE


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ("name", "phone_number", "status", "source", "comment")
        labels = {
            "name": "Имя",
            "phone_number": "Телефон",
            "status": "Статус",
            "source": "Источник",
            "comment": "Комментарий",
        }
        error_messages = {
            "phone_number": {
                "unique": "Лид с таким номером телефона уже существует.",
            },
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
                attrs={"type": "date"},
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


class SalesFunnelForm(forms.Form):
    start_date = forms.DateField(
        label="С:",
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
    )
    end_date = forms.DateField(
        label="До:",
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
    )
    source = forms.ChoiceField(
        label="Источник:",
        choices=LEAD_SOURCE,
        required=False,
    )
