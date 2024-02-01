from django.shortcuts import render
from leads.models import Lead


def index(request):
    template = "index/index.html"
    leads = Lead.objects.order_by("-date_of_creation")[:10]
    context = {
        "leads": leads,
    }
    return render(request, template, context)
