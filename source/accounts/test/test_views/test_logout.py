from accounts.factory.user_factory import UserFactory
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class TestLogout(TestCase):

    def setUp(self):
        self.user = UserFactory.create(email="test@example.com", password="password123")
        self.client.login(username="test@example.com", password="password123")
        self.logout_url = reverse("accounts:logout")

    def test_logout_valid_user(self):
        response = self.client.post(self.logout_url)
        self.assertRedirects(response, reverse("part:parts_list"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("Вы вышли из аккаунта" in str(message) for message in messages)
        )
