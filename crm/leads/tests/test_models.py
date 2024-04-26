from django.test import TestCase
from leads.models import Lead
from leads.validators import phone_regex


class LeadModelTest(TestCase):
    def setUp(self):
        self.lead = Lead.objects.create(
            name="Иван", phone_number="+71234567890", source="Яндекс Директ"
        )

    def test_phone_number_validator(self):
        """Поле phone_number содержит валидатор phone_regex."""
        lead = self.lead
        validator = lead._meta.get_field("phone_number").validators[0]
        self.assertEqual(validator, phone_regex)
