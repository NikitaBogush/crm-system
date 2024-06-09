from datetime import date, timedelta
from rest_framework.generics import ListAPIView

from leads.models import Lead, Deal
from .serializers import LeadSerializer, DealSerializer


class LeadList(ListAPIView):
    """Лиды за вчерашний день."""

    queryset = Lead.objects.filter(
        date_of_creation__date=date.today() - timedelta(days=1)
    )
    serializer_class = LeadSerializer


class DealList(ListAPIView):
    """Сделки за вчерашний день."""

    queryset = Deal.objects.filter(
        date_of_deal__date=date.today() - timedelta(days=1)
    )
    serializer_class = DealSerializer
