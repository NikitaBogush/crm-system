from django.urls import path

from . import views

app_name = "leads"

urlpatterns = [
    # Редактирование сделки:
    path(
        "deals/<int:pk>/edit/",
        views.DealEditView.as_view(),
        name="deal_edit",
    ),
    # Редактирование задачи:
    path(
        "tasks/<int:pk>/edit/",
        views.TaskEditView.as_view(),
        name="task_edit",
    ),
    # Редактирование лида:
    path(
        "leads/<int:pk>/edit/", views.LeadEditView.as_view(), name="lead_edit"
    ),
    # Создание сделки:
    path(
        "leads/<lead_id>/deal-create/",
        views.DealCreateView.as_view(),
        name="deal_create",
    ),
    # Создание задачи:
    path(
        "leads/<lead_id>/task-create/",
        views.TaskCreateView.as_view(),
        name="task_create",
    ),
    # Создание лида:
    path("leads/create/", views.LeadCreateView.as_view(), name="lead_create"),
    # Страница лида:
    path(
        "leads/<int:pk>/", views.LeadDetailView.as_view(), name="lead_detail"
    ),
    # Воронка продаж:
    path("sales-funnel/", views.sales_funnel, name="sales_funnel"),
    # Поиск лида по номеру телефона:
    path("search/", views.search, name="search"),
    # Сделки:
    path("deals/", views.DealsView.as_view(), name="deals"),
    # Задачи:
    path("tasks/", views.TasksView.as_view(), name="tasks"),
    # Лиды:
    path("leads/", views.LeadsView.as_view(), name="leads"),
    # Главная:
    path("", views.index, name="index"),
]
