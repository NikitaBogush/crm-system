from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from leads.models import Lead, Task, Deal

User = get_user_model()


class LeadFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="User123")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_lead(self):
        """Валидная форма создает новую запись в модели Lead."""
        # Подсчитываем количество записей в Lead:
        lead_count = Lead.objects.count()
        form_data = {
            "name": "Иван",
            "phone_number": "+71234567890",
            "status": "1",
            "source": "Яндекс Директ",
            "comment": "",
        }
        response = self.authorized_client.post(
            reverse("leads:lead_create"), data=form_data, follow=True
        )
        # Проверяем, сработал ли редирект:
        self.assertRedirects(
            response, reverse("leads:lead_detail", kwargs={"pk": 1})
        )
        # Проверяем, увеличилось ли число лидов:
        self.assertEqual(Lead.objects.count(), lead_count + 1)

    def test_edit_lead(self):
        """Валидная форма редактирует запись в модели Lead."""
        self.lead = Lead.objects.create(
            name="Иван", phone_number="+71234567890", source="Яндекс Директ"
        )
        form_data = {
            "name": "Иван",
            "phone_number": "+71234567890",
            "status": "1",
            "source": "Яндекс Директ",
            "comment": "Новый комментарий",
        }
        response = self.authorized_client.post(
            reverse("leads:lead_edit", kwargs={"pk": self.lead.pk}),
            data=form_data,
            follow=True,
        )
        # Проверяем, сработал ли редирект:
        self.assertRedirects(
            response, reverse("leads:lead_detail", kwargs={"pk": self.lead.pk})
        )
        # Проверяем, изменились ли данные в объекте Lead:
        self.assertEqual(
            Lead.objects.get(id=self.lead.id).comment, "Новый комментарий"
        )


class TaskFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="User123")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        # создаем Лид для возможности создания Задачи:
        self.lead = Lead.objects.create(
            name="Иван", phone_number="+71234567890", source="Яндекс Директ"
        )

    def test_create_task(self):
        """Валидная форма создает новую запись в модели Task."""
        # Подсчитываем количество записей в Task:
        task_count = Task.objects.count()
        form_data = {
            "name": "Позвонить",
            "comment": "Нужно позвонить",
            "task_date": date.today(),
        }
        response = self.authorized_client.post(
            reverse("leads:task_create", kwargs={"lead_id": self.lead.pk}),
            data=form_data,
            follow=True,
        )
        # Проверяем, сработал ли редирект:
        self.assertRedirects(
            response, reverse("leads:lead_detail", kwargs={"pk": self.lead.pk})
        )
        # Проверяем, увеличилось ли число задач:
        self.assertEqual(Lead.objects.count(), task_count + 1)

    def test_edit_task(self):
        """Валидная форма редактирует запись в модели Task."""
        self.task = Task.objects.create(
            lead=self.lead, name="Позвонить", comment="Нужно позвонить"
        )
        form_data = {
            "name": "Позвонить",
            "comment": "Новый комментарий",
            "task_date": date.today(),
        }
        response = self.authorized_client.post(
            reverse("leads:task_edit", kwargs={"pk": self.task.pk}),
            data=form_data,
            follow=True,
        )
        # Проверяем, сработал ли редирект:
        self.assertRedirects(
            response, reverse("leads:lead_detail", kwargs={"pk": self.lead.pk})
        )
        # Проверяем, изменились ли данные в объекте Task:
        self.assertEqual(
            Task.objects.get(id=self.task.id).comment, "Новый комментарий"
        )

    def test_task_create_task_date_error(self):
        """Проверяем, что при создании задачи нельзя установить дату
        в прошлом.
        """
        # Подсчитываем количество записей в Task:
        task_count = Task.objects.count()
        form_data = {
            "name": "Позвонить",
            "comment": "Нужно позвонить",
            # Указываем дату в прошлом:
            "task_date": date.today() - timedelta(days=1),
        }
        response = self.authorized_client.post(
            reverse("leads:task_create", kwargs={"lead_id": self.lead.pk}),
            data=form_data,
            follow=True,
        )
        # Проверяем, что число задач не увеличилось:
        self.assertEqual(Task.objects.count(), task_count)
        # Проверим, что форма вернула ошибку с ожидаемым текстом:
        self.assertFormError(
            response.context["form"],
            "task_date",
            "Нельзя установить дату в прошлом",
        )
        # Проверим, что ничего не упало и страница отдаёт код 200:
        self.assertEqual(response.status_code, 200)

    def test_task_edit_task_date_error(self):
        """Проверяем, что при редактировании задачи
        нельзя установить дату задачи раньше даты создания этой задачи.
        """
        self.task = Task.objects.create(
            lead=self.lead, name="Позвонить", comment="Нужно позвонить"
        )
        form_data = {
            "name": "Позвонить",
            "comment": "Нужно позвонить",
            # Указываем дату задачи раньше даты создания задачи:
            "task_date": date.today() - timedelta(days=1),
        }
        response = self.authorized_client.post(
            reverse("leads:task_edit", kwargs={"pk": self.task.pk}),
            data=form_data,
            follow=True,
        )
        # Проверим, что форма вернула ошибку с ожидаемым текстом:
        self.assertFormError(
            response.context["form"],
            "task_date",
            "Нельзя установить дату задачи раньше даты создания этой задачи",
        )
        # Проверим, что ничего не упало и страница отдаёт код 200:
        self.assertEqual(response.status_code, 200)


class DealFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="User123")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        # Создаем Лид для возможности создания Сделки:
        self.lead = Lead.objects.create(
            name="Иван", phone_number="+71234567890", source="Яндекс Директ"
        )

    def test_create_deal(self):
        """Валидная форма создает новую запись в модели Deal."""
        # Подсчитываем количество записей в Deal:
        deal_count = Deal.objects.count()
        form_data = {
            "name": "Продажа",
            "total": 3500,
        }
        response = self.authorized_client.post(
            reverse("leads:deal_create", kwargs={"lead_id": self.lead.pk}),
            data=form_data,
            follow=True,
        )
        # Проверяем, сработал ли редирект:
        self.assertRedirects(
            response, reverse("leads:lead_detail", kwargs={"pk": self.lead.pk})
        )
        # Проверяем, увеличилось ли число задач:
        self.assertEqual(Lead.objects.count(), deal_count + 1)

    def test_edit_deal(self):
        """Валидная форма редактирует запись в модели Deal."""
        self.deal = Deal.objects.create(
            name="Продажа", total=3500, lead=self.lead
        )
        form_data = {
            "name": "Продажа",
            "total": 5000,
        }
        response = self.authorized_client.post(
            reverse("leads:deal_edit", kwargs={"pk": self.deal.pk}),
            data=form_data,
            follow=True,
        )
        # Проверяем, сработал ли редирект:
        self.assertRedirects(
            response, reverse("leads:lead_detail", kwargs={"pk": self.lead.pk})
        )
        # Проверяем, изменились ли данные в объекте Deal:
        self.assertEqual(Deal.objects.get(id=self.deal.id).total, 5000)


class SalesFunnelFormTests(TestCase):
    def setUp(self):
        self.lead = Lead.objects.create(
            name="Иван",
            phone_number="+71234567890",
            source="Яндекс Директ",
            status="2",
        )
        self.deal = Deal.objects.create(
            name="Продажа", total=3500, lead=self.lead
        )
        self.user = User.objects.create_user(username="User123")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_sales_funnel_page_show_correct_context(self):
        """Шаблон sales_funnel сформирован с правильным контекстом."""
        form_data = {
            "start_date": date.today(),
            "end_date": date.today(),
            "source": "Яндекс Директ",
        }
        response = self.authorized_client.get(
            reverse("leads:sales_funnel"),
            data=form_data,
            follow=True,
        )
        self.assertEqual(response.context["new_leads_count"], 1)
        self.assertEqual(response.context["new_leads_with_deals_count"], 1)
        self.assertEqual(response.context["conversion"], 100)
        self.assertEqual(response.context["sum"], 3500)
        self.assertEqual(response.context["average_bill"], 3500)

    def test_end_date_error(self):
        form_data = {
            "start_date": date.today(),
            # Указываем некорректную дату окончания:
            "end_date": date.today() - timedelta(days=1),
            "source": "Яндекс Директ",
        }
        response = self.authorized_client.get(
            reverse("leads:sales_funnel"),
            data=form_data,
            follow=True,
        )
        # Проверим, что форма вернула ошибку с ожидаемым текстом:
        self.assertFormError(
            response.context["form"],
            "end_date",
            "Дата окончания не может быть раньше даты начала",
        )
        # Проверим, что ничего не упало и страница отдаёт код 200:
        self.assertEqual(response.status_code, 200)


class SearchFormTests(TestCase):
    def setUp(self):
        self.lead = Lead.objects.create(
            name="Иван", phone_number="+71234567890", source="Яндекс Директ"
        )
        self.user = User.objects.create_user(username="User123")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_search_redirect(self):
        """Проверяем редирект при отправке формы Search"""
        form_data = {"q": "+71234567890"}
        response = self.authorized_client.get(
            reverse("leads:search"),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response, reverse("leads:lead_detail", kwargs={"pk": self.lead.pk})
        )
