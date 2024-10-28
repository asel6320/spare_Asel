from http import HTTPStatus

from django.urls import reverse
from django.test import TestCase

from accounts.factory.user_factory import UserFactory
from accounts.forms.registration import RegisterForm


class TestRegister(TestCase):

    def setUp(self):
        self.user = UserFactory.create(password="password")
        self.client.login(username=self.user.username, password="password")

    def test_get_register_view(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")
        self.assertIsInstance(response.context["form"], RegisterForm)

    def test_post_register_view(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "user2",
                "password1": "password2",
                "password2": "password2",
                "phone_number": "1234567890",
            },
        )
        self.assertRedirects(response, reverse("webapp:parts_list"))
