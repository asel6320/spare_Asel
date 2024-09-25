from django.urls import reverse
from django.test import TestCase

from accounts.factory.user_factory import UserFactory
from accounts.forms.user_update_form import UserUpdateForm


class TestProfile(TestCase):

    def setUp(self):
        self.user = UserFactory.create(password='password')
        self.client.login(username=self.user.username, password='password')

    def test_get_profile_edit_view(self):
        response = self.client.get(reverse('profile_edit_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_edit.html')
        self.assertIsInstance(response.context['form'], UserUpdateForm)
        self.assertEqual(response.context['form'].instance, self.user)

    def test_post_profile_edit_view(self):
        response = self.client.post(reverse('profile_edit_view'),
                                    {
                                        'username': 'user2',
                                        'phone_number': '123456789',
                                    })
        self.assertRedirects(response, reverse('profile_view'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'user2')
        self.assertEqual(self.user.phone_number, '123456789')

