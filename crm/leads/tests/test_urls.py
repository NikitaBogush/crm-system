from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from leads.models import Lead, Task, Deal

User = get_user_model()


class LeadURLTests(TestCase):
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
        self.guest_client = Client()
        self.user = User.objects.create_user(username="User123")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_status_code_authorized(self):
        """Проверяем доступность страниц для авторизованного пользователя."""
        urls = [
            f"/deals/{self.deal.pk}/edit/",
            f"/tasks/{self.task.pk}/edit/",
            f"/leads/{self.lead.pk}/edit/",
            f"/leads/{self.lead.pk}/deal-create/",
            f"/leads/{self.lead.pk}/task-create/",
            "/leads/create/",
            f"/leads/{self.lead.pk}/",
            "/sales-funnel/",
            "/deals/",
            "/tasks/",
            "/leads/",
            "/",
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_redirect_anonymous(self):
        """Проверяем редиректы страниц для неавторизованного пользователя."""
        urls = [
            f"/deals/{self.deal.pk}/edit/",
            f"/tasks/{self.task.pk}/edit/",
            f"/leads/{self.lead.pk}/edit/",
            f"/leads/{self.lead.pk}/deal-create/",
            f"/leads/{self.lead.pk}/task-create/",
            "/leads/create/",
            f"/leads/{self.lead.pk}/",
            "/sales-funnel/",
            "/deals/",
            "/tasks/",
            "/leads/",
            "/",
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url, follow=True)
                self.assertRedirects(response, f"/auth/login/?next={url}")

    def test_templates(self):
        """Проверяем соответствие url и вызываемого шаблона."""
        url_templates = {
            f"/deals/{self.deal.pk}/edit/": "leads/deal_create.html",
            f"/tasks/{self.task.pk}/edit/": "leads/task_create.html",
            f"/leads/{self.lead.pk}/edit/": "leads/lead_create.html",
            f"/leads/{self.lead.pk}/deal-create/": "leads/deal_create.html",
            f"/leads/{self.lead.pk}/task-create/": "leads/task_create.html",
            "/leads/create/": "leads/lead_create.html",
            f"/leads/{self.lead.pk}/": "leads/lead_detail.html",
            "/sales-funnel/": "leads/sales-funnel.html",
            "/deals/": "leads/deals.html",
            "/tasks/": "leads/tasks.html",
            "/leads/": "leads/leads.html",
            "/": "leads/index.html",
        }
        for url, template in url_templates.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
