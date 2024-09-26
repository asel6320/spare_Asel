from django.test import TestCase
from django.urls import reverse
from webapp.models import Cart, Part, VehicleInfo, Category

from accounts.factory.user_factory import UserFactory


class TestCart(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create(password='password')

    def setUp(self):
        self.category = Category.objects.create(name='Category1')
        self.vehicle_info = VehicleInfo.objects.create(name='VehicleInfo1')
        self.part = Part.objects.create(
            category=self.category,
            vehicle_info=self.vehicle_info,
            name='Part1',
            description='Part_description1',
            amount=5
        )

    def test_cart_add_non_authenticated_user(self):
        response = self.client.post(reverse('webapp:part_add_cart', kwargs={'pk': self.part.pk}))
        self.assertEqual(response.status_code, 302)