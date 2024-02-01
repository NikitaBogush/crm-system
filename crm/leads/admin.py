from django.contrib import admin

from .models import Lead


class LeadAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ("name", "phone_number", "date_of_creation")
    # Добавляем интерфейс для поиска по номеру телефона
    search_fields = ("phone_number",)
    # Добавляем возможность фильтрации по дате
    list_filter = ("date_of_creation",)


admin.site.register(Lead, LeadAdmin)
