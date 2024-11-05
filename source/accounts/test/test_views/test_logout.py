from accounts.factory.user_factory import UserFactory
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class TestLogout(TestCase):

    def setUp(self):
        self.user = UserFactory.create(password="password")
        self.client.login(username=self.user.username, password="password")
        self.logout_url = reverse("accounts:logout")

    def test_logout_valid_user(self):
        response = self.client.post(self.logout_url)
        self.assertRedirects(response, reverse("part:parts_list"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            messages[0].message, f"{self.user.username} - Вы вышли из аккаунта"
        )

    def test_logout_anonymous_user(self):
        self.client.logout()
        response = self.client.post(self.logout_url)
        self.assertRedirects(response, reverse("part:parts_list"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
