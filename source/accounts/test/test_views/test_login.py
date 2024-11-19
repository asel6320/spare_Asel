from accounts.factory.user_factory import UserFactory
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class TestLogin(TestCase):

    def setUp(self):
        self.user = UserFactory.create(email="test@example.com", password="password123")

    def test_login_valid_user(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "test@example.com", "password": "password123"},
        )
        self.assertRedirects(response, reverse("part:parts_list"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_invalid_user(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "test@example.com", "password": "wrong_password"},
        )
        self.assertFalse(response.wsgi_request.user.is_authenticated)
