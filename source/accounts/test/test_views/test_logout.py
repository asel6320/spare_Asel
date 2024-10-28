from django.urls import reverse
from django.test import TestCase

from accounts.factory.user_factory import UserFactory


class TestLogout(TestCase):

    def setUp(self):
        self.user = UserFactory.create(password="password")

    def test_correct_logout(self):
        response = self.client.post(
            reverse("logout"), {"username": self.user.username, "password": "password"}
        )
        self.assertRedirects(response, reverse("webapp:parts_list"))
