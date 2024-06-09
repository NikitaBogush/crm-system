from rest_framework import serializers

from leads.models import Lead, Deal


class LeadSerializer(serializers.ModelSerializer):
    """Сериализатор для списка лидов за вчерашний день."""

    class Meta:
        model = Lead
        fields = ("name", "phone_number", "date_of_creation")


class DealSerializer(serializers.ModelSerializer):
    """Сериализатор для списка сделок за вчерашний день."""

    class Meta:
        model = Deal
        fields = ("name", "total", "date_of_deal")
