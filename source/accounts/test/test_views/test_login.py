from django.urls import reverse
from django.test import TestCase

from accounts.factory.user_factory import UserFactory


class TestLogin(TestCase):

    def setUp(self):
        self.user = UserFactory.create(password="password")

    def test_correct_login(self):
        response = self.client.post(
            reverse("login"), {"username": self.user.username, "password": "password"}
        )
        self.assertRedirects(response, reverse("webapp:parts_list"))
