from accounts.factory.user_factory import UserFactory
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class TestLogin(TestCase):

    def setUp(self):
        self.user = UserFactory.create(password="password")
        self.login_url = reverse("accounts:login")
        self.valid_data = {"username": self.user.username, "password": "password"}

    def test_login_valid_user(self):
        response = self.client.post(self.login_url, self.valid_data)
        self.assertRedirects(response, reverse("part:parts_list"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_invalid_user(self):
        invalid_data = {"username": "invaliduser", "password": "wrongpassword"}
        response = self.client.post(self.login_url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
