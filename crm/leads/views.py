from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import LeadForm


class CreateLeadView(CreateView):
    form_class = LeadForm
    template_name = "leads/create_lead.html"
    success_url = "index/index.html"  # изменить позднее
