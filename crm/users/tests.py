from django.contrib.auth import get_user_model
from django.test import TestCase, Client

User = get_user_model()


class LeadURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username="User123")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_status_code_login_anonymous(self):
        """Проверяем доступность страницы login для неавторизованного
        пользователя"""

        response = self.guest_client.get("/auth/login/")
        self.assertEqual(response.status_code, 200)

    def test_status_code_logout_authorized(self):
        """Проверяем доступность страницы logout для авторизованного
        пользователя"""

        response = self.authorized_client.post("/auth/logout/")
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        """Проверяем соответствие url и вызываемого шаблона"""

        response = self.guest_client.get("/auth/login/")
        self.assertTemplateUsed(response, "users/login.html")

        response = self.authorized_client.post("/auth/logout/")
        self.assertTemplateUsed(response, "users/logged_out.html")
