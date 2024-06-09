from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    # Лиды за вчерашний день:
    path("leads/", views.LeadList.as_view(), name="leads"),
    # Сделки за вчерашний день:
    path("deals/", views.DealList.as_view(), name="deals"),
]
