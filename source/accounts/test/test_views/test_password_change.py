from django.urls import reverse
from django.test import TestCase

from accounts.factory.user_factory import UserFactory


class TestPasswordChange(TestCase):

    def setUp(self):
        self.user = UserFactory.create(password="old_password")
        self.client.login(username=self.user.username, password="old_password")
        self.url = reverse("password_change")

    def test_password_change_view_renders_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "change_password.html")

    def test_password_change_success(self):
        response = self.client.post(
            self.url,
            {
                "old_password": "old_password",
                "new_password1": "new_password_123",
                "new_password2": "new_password_123",
            },
        )
        self.assertRedirects(response, reverse("profile_view"))

        self.client.logout()
        login_successful = self.client.login(
            username=self.user.username, password="new_password_123"
        )
        self.assertTrue(login_successful)

    def test_password_change_invalid_old_password(self):
        response = self.client.post(
            self.url,
            {
                "old_password": "wrong_old_password",
                "new_password1": "new_password_123",
                "new_password2": "new_password_123",
            },
        )
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            form,
            "old_password",
            "Your old password was entered incorrectly. Please enter it again.",
        )

    def test_password_change_mismatched_new_passwords(self):
        response = self.client.post(
            self.url,
            {
                "old_password": "old_password",
                "new_password1": "new_password_123",
                "new_password2": "different_password",
            },
        )
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            form, "new_password2", "The two password fields didn’t match."
        )
