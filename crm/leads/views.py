from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.list import MultipleObjectMixin
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.contrib import messages
from .forms import LeadForm, TaskForm, DealForm, SalesFunnelForm
from .models import Lead, Task, Deal


from datetime import datetime, date, timedelta


@login_required
def index(request):
    start_date = datetime.today() - timedelta(days=7)
    end_date = datetime.today()
    tasks_count = (
        Task.objects.filter(active=True)
        .filter(task_date__lte=datetime.today())
        .count()
    )
    leads_count = Lead.objects.filter(
        date_of_creation__range=(start_date, end_date)
    ).count()
    deals_count = Deal.objects.filter(
        date_of_deal__range=(start_date, end_date)
    ).count()
    deals_sum = Deal.objects.filter(
        date_of_deal__range=(start_date, end_date)
    ).aggregate(Sum("total"))["total__sum"]
    template = "leads/index.html"
    context = {
        "tasks_count": tasks_count,
        "leads_count": leads_count,
        "deals_count": deals_count,
        "deals_sum": deals_sum,
    }
    return render(request, template, context)


class LeadsView(LoginRequiredMixin, ListView):
    model = Lead
    template_name = "leads/leads.html"
    paginate_by = 10


class TasksView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "leads/tasks.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["overdue_tasks"] = Task.objects.filter(active=True).filter(
            task_date__lt=datetime.today()
        )
        context["scheduled_tasks"] = Task.objects.filter(active=True).filter(
            task_date=datetime.today()
        )
        return context


class DealsView(LoginRequiredMixin, ListView):
    model = Deal
    template_name = "leads/deals.html"
    paginate_by = 10


@login_required
def sales_funnel(request):
    form = SalesFunnelForm(request.GET or None)
    context = {"form": form}
    if form.is_valid():
        if form.cleaned_data["end_date"] < form.cleaned_data["start_date"]:
            form.add_error(
                "end_date",
                "Дата окончания не может быть раньше даты начала",
            )
            return render(request, "leads/sales-funnel.html", context)
        start_date = form.cleaned_data["start_date"]
        end_date = form.cleaned_data["end_date"] + timedelta(days=1)
        source = form.cleaned_data["source"]
        if source == "":
            new_leads_count = Lead.objects.filter(
                date_of_creation__range=(start_date, end_date)
            ).count()
            new_leads_with_deals = Lead.objects.filter(
                date_of_creation__range=(start_date, end_date)
            ).filter(status="2")
        else:
            new_leads_count = (
                Lead.objects.filter(
                    date_of_creation__range=(start_date, end_date)
                )
                .filter(source=source)
                .count()
            )
            new_leads_with_deals = (
                Lead.objects.filter(
                    date_of_creation__range=(start_date, end_date)
                )
                .filter(source=source)
                .filter(status="2")
            )
        new_leads_with_deals_count = new_leads_with_deals.count()
        try:
            conversion = round(
                (new_leads_with_deals_count / new_leads_count) * 100
            )
        except ZeroDivisionError:
            conversion = 0
        sum = Deal.objects.filter(lead__in=new_leads_with_deals).aggregate(
            Sum("total")
        )["total__sum"]
        if sum is None:
            sum = 0
        try:
            average_bill = round(sum / new_leads_with_deals_count)
        except ZeroDivisionError:
            average_bill = 0
        context = {
            "new_leads_count": new_leads_count,
            "new_leads_with_deals_count": new_leads_with_deals_count,
            "conversion": conversion,
            "sum": sum,
            "average_bill": average_bill,
            "form": form,
        }
        return render(request, "leads/sales-funnel.html", context)
    return render(request, "leads/sales-funnel.html", context)


class LeadDetailView(LoginRequiredMixin, DetailView, MultipleObjectMixin):
    model = Lead
    paginate_by = 5

    def get_context_data(self, **kwargs):
        completed_tasks = (
            Task.objects.filter(lead=self.object)
            .filter(active=False)
            .order_by("-task_date")
        )
        context = super().get_context_data(
            object_list=completed_tasks, **kwargs
        )
        context["overdue_tasks"] = (
            Task.objects.filter(lead=self.object)
            .filter(active=True)
            .filter(task_date__lt=datetime.today())
        )
        context["scheduled_tasks"] = (
            Task.objects.filter(lead=self.object)
            .filter(active=True)
            .filter(task_date__gte=datetime.today())
        )
        context["deals"] = Deal.objects.filter(lead=self.object).order_by(
            "-date_of_deal"
        )
        return context


class LeadCreateView(LoginRequiredMixin, CreateView):
    form_class = LeadForm
    template_name = "leads/lead_create.html"

    def form_valid(self, form):
        lead = form.save()
        return redirect(lead)


class LeadEditView(LoginRequiredMixin, UpdateView):
    form_class = LeadForm
    model = Lead
    template_name = "leads/lead_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = True
        context["lead"] = self.object
        return context

    def form_valid(self, form):
        lead = form.save()
        return redirect(lead)


class TaskCreateView(LoginRequiredMixin, CreateView):
    form_class = TaskForm
    template_name = "leads/task_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lead"] = Lead.objects.get(pk=self.kwargs["lead_id"])
        return context

    def form_valid(self, form):
        if form.cleaned_data["task_date"] < date.today():
            form.add_error("task_date", "Нельзя установить дату в прошлом")
            return self.form_invalid(form)
        elif "complete_create_submit" in self.request.POST:
            task = form.save(commit=False)
            task.lead = Lead.objects.get(pk=self.kwargs["lead_id"])
            task.active = False
            task.save()
            return redirect("leads:task_create", task.lead.pk)
        elif "complete_submit" in self.request.POST:
            task = form.save(commit=False)
            task.lead = Lead.objects.get(pk=self.kwargs["lead_id"])
            task.active = False
            task.save()
            return redirect("leads:lead_detail", task.lead.pk)
        else:
            task = form.save(commit=False)
            task.lead = Lead.objects.get(pk=self.kwargs["lead_id"])
            task.save()
            return redirect("leads:lead_detail", task.lead.pk)


class TaskEditView(LoginRequiredMixin, UpdateView):
    form_class = TaskForm
    model = Task
    template_name = "leads/task_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lead"] = Lead.objects.get(tasks=self.object)
        context["is_edit"] = True
        return context

    def form_valid(self, form):
        if form.cleaned_data["task_date"] < self.object.date_of_creation:
            form.add_error(
                "task_date",
                "Нельзя установить дату задачи раньше даты создания этой задачи",
            )
            return self.form_invalid(form)
        elif "complete_create_submit" in self.request.POST:
            task = form.save(commit=False)
            task.active = False
            task.save()
            return redirect("leads:task_create", task.lead.pk)
        elif "complete_submit" in self.request.POST:
            task = form.save(commit=False)
            task.active = False
            task.save()
            return redirect("leads:lead_detail", task.lead.pk)
        else:
            task = form.save()
            return redirect("leads:lead_detail", task.lead.pk)


class DealCreateView(LoginRequiredMixin, CreateView):
    form_class = DealForm
    template_name = "leads/deal_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lead"] = Lead.objects.get(pk=self.kwargs["lead_id"])
        return context

    def form_valid(self, form):
        deal = form.save(commit=False)
        deal.lead = Lead.objects.get(pk=self.kwargs["lead_id"])
        deal.lead.status = "2"
        deal.lead.save()
        deal.save()
        return redirect("leads:lead_detail", deal.lead.pk)


class DealEditView(LoginRequiredMixin, UpdateView):  # доработать html-шаблон
    form_class = DealForm
    model = Deal
    template_name = "leads/deal_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lead"] = Lead.objects.get(deals=self.object)
        context["is_edit"] = True
        return context

    def form_valid(self, form):
        deal = form.save()
        return redirect("leads:lead_detail", deal.lead.pk)


@login_required
def search(request):
    query = request.GET.get("q")
    lead = get_object_or_404(Lead, phone_number__exact=query)
    return redirect("leads:lead_detail", lead.pk)
