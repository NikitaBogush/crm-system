from django.shortcuts import redirect, render
from django.views.generic import DetailView, CreateView
from django.urls import reverse_lazy
from .forms import LeadForm
from .models import Lead


class CreateLeadView(CreateView):
    form_class = LeadForm
    template_name = "leads/create_lead.html"

    def form_valid(self, form):
        lead = form.save()
        return redirect(lead)


class LeadDetailView(DetailView):
    model = Lead
