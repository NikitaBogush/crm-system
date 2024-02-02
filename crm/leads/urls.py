from django.urls import path
from . import views

app_name = "leads"

urlpatterns = [
    path("<int:pk>/", views.LeadDetailView.as_view(), name="lead_detail"),
    path("create/", views.CreateLeadView.as_view(), name="create_lead"),
]
