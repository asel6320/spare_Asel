from django.urls import reverse
from django.test import TestCase

from accounts.factory.user_factory import UserFactory


class TestProfileView(TestCase):

    def setUp(self):
        self.user = UserFactory.create(password='password')
        self.client.login(username=self.user.username, password='password')

    def test_profile_view_get(self):
        response = self.client.get(reverse('profile_view'))
        self.assertTemplateUsed(response, template_name='profile_view.html')