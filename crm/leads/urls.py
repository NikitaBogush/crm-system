from django.urls import path
from . import views

app_name = "leads"

urlpatterns = [
    path(
        "leads/<lead_id>/tasks/create/",
        views.TaskCreateView.as_view(),
        name="task_create",
    ),
    path(
        "leads/<int:pk>/", views.LeadDetailView.as_view(), name="lead_detail"
    ),
    path("leads/create/", views.LeadCreateView.as_view(), name="lead_create"),
    path("", views.index, name="index"),
]
