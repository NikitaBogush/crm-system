from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import LeadForm, TaskForm, DealForm
from .models import Lead, Task, Deal

from datetime import datetime


@login_required
def index(request):
    # доработать функцию
    template = "leads/index.html"
    leads = Lead.objects.order_by("-date_of_creation")[:10]
    context = {
        "leads": leads,
    }
    return render(request, template, context)


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


class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["overdue_tasks"] = (
            Task.objects.filter(lead=self.object)
            .filter(active=True)
            .filter(task_date__lt=datetime.today())
            .order_by("task_date")
        )
        context["scheduled_tasks"] = (
            Task.objects.filter(lead=self.object)
            .filter(active=True)
            .filter(task_date__gte=datetime.today())
            .order_by("task_date")
        )
        context["completed_tasks"] = (
            Task.objects.filter(lead=self.object)
            .filter(active=False)
            .order_by("-task_date")
        )
        context["deals"] = Deal.objects.filter(lead=self.object).order_by(
            "-date_of_deal"
        )
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    form_class = TaskForm
    template_name = "leads/task_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lead"] = Lead.objects.get(pk=self.kwargs["lead_id"])
        return context

    def form_valid(self, form):
        if "complete_create_submit" in self.request.POST:
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
        if "complete_create_submit" in self.request.POST:
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


class TasksView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "leads/tasks.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["overdue_tasks"] = (
            Task.objects.filter(active=True)
            .filter(task_date__lt=datetime.today())
            .order_by("task_date")
        )
        context["scheduled_tasks"] = (
            Task.objects.filter(active=True)
            .filter(task_date=datetime.today())
            .order_by("task_date")
        )
        return context


class LeadsView(LoginRequiredMixin, ListView):
    model = Lead
    template_name = "leads/leads.html"


@login_required
def search(request):
    query = request.GET.get("q")
    lead = get_object_or_404(Lead, phone_number__exact=query)
    return redirect("leads:lead_detail", lead.pk)
