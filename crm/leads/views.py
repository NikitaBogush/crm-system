from django.shortcuts import redirect, render
from django.views.generic import DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import LeadForm, TaskForm
from .models import Lead, Task


def index(request):
    template = "leads/index.html"
    leads = Lead.objects.order_by("-date_of_creation")[:10]
    context = {
        "leads": leads,
    }
    return render(request, template, context)


class LeadCreateView(CreateView):
    form_class = LeadForm
    template_name = "leads/lead_create.html"

    def form_valid(self, form):
        lead = form.save()
        return redirect(lead)


class LeadDetailView(DetailView):
    model = Lead

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = Task.objects.filter(lead=self.object)
        return context


class TaskCreateView(CreateView):
    form_class = TaskForm
    template_name = "leads/task_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lead"] = Lead.objects.get(pk=self.kwargs["lead_id"])
        return context

    def form_valid(self, form):
        task = form.save(commit=False)
        task.lead = Lead.objects.get(pk=self.kwargs["lead_id"])
        task.save()
        return redirect("leads:lead_detail", task.lead.pk)


class TaskEditView(UpdateView):
    form_class = TaskForm
    model = Task
    template_name = "leads/task_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lead"] = Lead.objects.get(tasks=self.object)
        context["is_edit"] = True
        return context

    def form_valid(self, form):
        task = form.save()
        return redirect("leads:lead_detail", task.lead.pk)
