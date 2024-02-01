from django.urls import path
from . import views

app_name = "leads"

urlpatterns = [
    path("create", views.CreateLeadView.as_view(), name="create_lead"),
]
