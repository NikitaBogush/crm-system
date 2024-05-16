from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from leads.models import Lead, Task, Deal

User = get_user_model()


class LeadViewTests(TestCase):
    def setUp(self):
        self.lead = Lead.objects.create(
            name="Иван", phone_number="+71234567890", source="Яндекс Директ"
        )
        self.task = Task.objects.create(
            lead=self.lead, name="Позвонить", comment="Нужно позвонить"
        )
        self.deal = Deal.objects.create(
            name="Продажа", total=3500, lead=self.lead
        )
        self.user = User.objects.create_user(username="User123")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """Проверяем соответствие url и вызываемого шаблона."""
        url_templates = {
            reverse(
                "leads:deal_edit", kwargs={"pk": self.deal.pk}
            ): "leads/deal_create.html",
            reverse(
                "leads:task_edit", kwargs={"pk": self.task.pk}
            ): "leads/task_create.html",
            reverse(
                "leads:lead_edit", kwargs={"pk": self.lead.pk}
            ): "leads/lead_create.html",
            reverse(
                "leads:deal_create", kwargs={"lead_id": self.lead.pk}
            ): "leads/deal_create.html",
            reverse(
                "leads:task_create", kwargs={"lead_id": self.lead.pk}
            ): "leads/task_create.html",
            reverse("leads:lead_create"): "leads/lead_create.html",
            reverse(
                "leads:lead_detail", kwargs={"pk": self.lead.pk}
            ): "leads/lead_detail.html",
            reverse("leads:sales_funnel"): "leads/sales-funnel.html",
            reverse("leads:deals"): "leads/deals.html",
            reverse("leads:tasks"): "leads/tasks.html",
            reverse("leads:leads"): "leads/leads.html",
            reverse("leads:index"): "leads/index.html",
        }
        for reverse_name, template in url_templates.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse("leads:index"))
        tasks_count = response.context["tasks_count"]
        leads_count = response.context["leads_count"]
        deals_count = response.context["deals_count"]
        deals_sum = response.context["deals_sum"]
        self.assertEqual(tasks_count, 1)
        self.assertEqual(leads_count, 1)
        self.assertEqual(deals_count, 1)
        self.assertEqual(deals_sum, 3500)

    def test_leads_page_show_correct_context(self):
        """Шаблон leads сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse("leads:leads"))
        first_object = response.context["object_list"][0]
        lead_name_0 = first_object.name
        lead_phone_number_0 = first_object.phone_number
        lead_status_0 = first_object.status
        lead_date_of_creation_0 = first_object.date_of_creation
        self.assertEqual(lead_name_0, "Иван")
        self.assertEqual(lead_phone_number_0, "+71234567890")
        self.assertEqual(lead_status_0, "1")
        self.assertEqual(
            lead_date_of_creation_0.date(), datetime.today().date()
        )

    def test_tasks_page_show_correct_context(self):
        """Шаблон tasks сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse("leads:tasks"))
        first_object = response.context["scheduled_tasks"][0]
        task_task_date_0 = first_object.task_date
        task_lead_0 = first_object.lead
        task_name_0 = first_object.name
        task_comment_0 = first_object.comment
        self.assertEqual(task_task_date_0, datetime.today().date())
        self.assertEqual(task_lead_0, self.lead)
        self.assertEqual(task_name_0, "Позвонить")
        self.assertEqual(task_comment_0, "Нужно позвонить")
        overdue_tasks = list(response.context["overdue_tasks"])
        self.assertEqual(overdue_tasks, [])

    def test_deals_page_show_correct_context(self):
        """Шаблон deals сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse("leads:deals"))
        first_object = response.context["object_list"][0]
        deal_lead_0 = first_object.lead
        deal_name_0 = first_object.name
        deal_date_of_deal_0 = first_object.date_of_deal
        deal_total_0 = first_object.total
        self.assertEqual(deal_lead_0, self.lead)
        self.assertEqual(deal_name_0, "Продажа")
        self.assertEqual(deal_date_of_deal_0.date(), datetime.today().date())
        self.assertEqual(deal_total_0, 3500)

    def test_sales_funnel_page_show_correct_context(self):
        """Шаблон sales_funnel сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse("leads:sales_funnel"))
        form_fields = {
            "start_date": forms.fields.DateField,
            "end_date": forms.fields.DateField,
            "source": forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get("form").fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_lead_detail_page_show_correct_context(self):
        """Шаблон lead_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse("leads:lead_detail", kwargs={"pk": self.lead.pk})
        )
        lead = response.context["lead"]
        lead_name = lead.name
        lead_phone_number = lead.phone_number
        lead_status = lead.status
        lead_source = lead.source
        lead_comment = lead.comment
        self.assertEqual(lead_name, "Иван")
        self.assertEqual(lead_phone_number, "+71234567890")
        self.assertEqual(lead_status, "1")
        self.assertEqual(lead_source, "Яндекс Директ")
        self.assertIsNone(lead_comment)
        object_list = list(response.context["object_list"])
        self.assertEqual(object_list, [])
        overdue_tasks = list(response.context["overdue_tasks"])
        self.assertEqual(overdue_tasks, [])
        scheduled_task = response.context["scheduled_tasks"][0]
        scheduled_task_task_date_0 = scheduled_task.task_date
        scheduled_task_name_0 = scheduled_task.name
        scheduled_task_comment_0 = scheduled_task.comment
        self.assertEqual(scheduled_task_task_date_0, datetime.today().date())
        self.assertEqual(scheduled_task_name_0, "Позвонить")
        self.assertEqual(scheduled_task_comment_0, "Нужно позвонить")
        deal = response.context["deals"][0]
        deal_date_of_deal_0 = deal.date_of_deal
        deal_name_0 = deal.name
        deal_total_0 = deal.total
        self.assertEqual(deal_date_of_deal_0.date(), datetime.today().date())
        self.assertEqual(deal_name_0, "Продажа")
        self.assertEqual(deal_total_0, 3500)

    def test_lead_create_page_show_correct_context(self):
        """Шаблон lead_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse("leads:lead_create"))
        form_fields = {
            "name": forms.fields.CharField,
            "phone_number": forms.fields.CharField,
            "status": forms.fields.ChoiceField,
            "source": forms.fields.ChoiceField,
            "comment": forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get("form").fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_task_create_page_show_correct_context(self):
        """Шаблон task_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse("leads:task_create", kwargs={"lead_id": self.lead.pk})
        )
        form_fields = {
            "name": forms.fields.CharField,
            "comment": forms.fields.CharField,
            "task_date": forms.fields.DateField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get("form").fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_deal_create_page_show_correct_context(self):
        """Шаблон deal_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse("leads:deal_create", kwargs={"lead_id": self.lead.pk})
        )
        form_fields = {
            "name": forms.fields.CharField,
            "total": forms.fields.IntegerField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get("form").fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_lead_edit_page_show_correct_context(self):
        """Шаблон lead_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse("leads:lead_edit", kwargs={"pk": self.lead.pk})
        )
        form_fields = {
            "name": forms.fields.CharField,
            "phone_number": forms.fields.CharField,
            "status": forms.fields.ChoiceField,
            "source": forms.fields.ChoiceField,
            "comment": forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get("form").fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_task_edit_page_show_correct_context(self):
        """Шаблон task_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse("leads:task_edit", kwargs={"pk": self.task.pk})
        )
        form_fields = {
            "name": forms.fields.CharField,
            "comment": forms.fields.CharField,
            "task_date": forms.fields.DateField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get("form").fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_deal_edit_page_show_correct_context(self):
        """Шаблон deal_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse("leads:deal_edit", kwargs={"pk": self.deal.pk})
        )
        form_fields = {
            "name": forms.fields.CharField,
            "total": forms.fields.IntegerField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get("form").fields.get(value)
                self.assertIsInstance(form_field, expected)


class PaginatorViewsTests(TestCase):
    def setUp(self):
        self.lead = Lead.objects.create(
            name="Иван", phone_number="+71234567880", source="Яндекс Директ"
        )
        self.task = Task.objects.create(
            lead=self.lead,
            name="Позвонить",
            comment="Нужно позвонить",
            active=False,
        )
        self.deal = Deal.objects.create(
            name="Продажа", total=3500, lead=self.lead
        )
        self.user = User.objects.create_user(username="User123")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        for count in range(10):
            Lead.objects.create(
                name="Иван",
                phone_number=f"+7123456789{count}",
                source="Яндекс Директ",
            )
            Task.objects.create(
                lead=self.lead,
                name="Позвонить",
                comment="Нужно позвонить",
                active=False,
            )
            Deal.objects.create(
                name="Продажа",
                total=3500,
                lead=self.lead,
            )

    def test_leads_first_page_has_ten_records(self):
        """Проверяем, что первая страница leads содержит 10 записей."""
        response = self.authorized_client.get(reverse("leads:leads"))
        self.assertEqual(len(response.context.get("page_obj").object_list), 10)

    def test_leads_second_page_has_one_records(self):
        """Проверяем, что вторая страница leads содержит 1 запись."""
        response = self.authorized_client.get(
            reverse("leads:leads") + "?page=2"
        )
        self.assertEqual(len(response.context.get("page_obj").object_list), 1)

    def test_deals_first_page_has_ten_records(self):
        """Проверяем, что первая страница deals содержит 10 записей."""
        response = self.authorized_client.get(reverse("leads:deals"))
        self.assertEqual(len(response.context.get("page_obj").object_list), 10)

    def test_deals_second_page_has_one_records(self):
        """Проверяем, что вторая страница deals содержит 1 запись."""
        response = self.authorized_client.get(
            reverse("leads:deals") + "?page=2"
        )
        self.assertEqual(len(response.context.get("page_obj").object_list), 1)

    def test_lead_detail_first_page_has_five_records(self):
        """Проверяем, что первая страница lead_detail содержит 5 записей."""
        response = self.authorized_client.get(
            reverse("leads:lead_detail", kwargs={"pk": self.lead.pk})
        )
        self.assertEqual(len(response.context.get("page_obj").object_list), 5)

    def test_lead_detail_third_page_has_one_records(self):
        """Проверяем, что третья страница lead_detail содержит 1 запись."""
        response = self.authorized_client.get(
            reverse("leads:lead_detail", kwargs={"pk": self.lead.pk})
            + "?page=3"
        )
        self.assertEqual(len(response.context.get("page_obj").object_list), 1)
