from django.urls import path
from . import views

app_name = "leads"

urlpatterns = [
    path(
        "deals/<int:pk>/edit/",
        views.DealEditView.as_view(),
        name="deal_edit",
    ),
    path(
        "tasks/<int:pk>/edit/",
        views.TaskEditView.as_view(),
        name="task_edit",
    ),
    path(
        "leads/<int:pk>/edit/", views.LeadEditView.as_view(), name="lead_edit"
    ),
    path(
        "leads/<lead_id>/deal-create/",
        views.DealCreateView.as_view(),
        name="deal_create",
    ),
    path(
        "leads/<lead_id>/task-create/",
        views.TaskCreateView.as_view(),
        name="task_create",
    ),
    path("leads/create/", views.LeadCreateView.as_view(), name="lead_create"),
    path(
        "leads/<int:pk>/", views.LeadDetailView.as_view(), name="lead_detail"
    ),
    path("sales-funnel/", views.sales_funnel, name="sales_funnel"),
    path("search/", views.search, name="search"),
    path("deals/", views.DealsView.as_view(), name="deals"),
    path("tasks/", views.TasksView.as_view(), name="tasks"),
    path("leads/", views.LeadsView.as_view(), name="leads"),
    path("", views.index, name="index"),
]
