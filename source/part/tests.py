from datetime import datetime

from accounts.factory import UserFactory
from django.test import TestCase
from django.urls import reverse
from favorite.models import Favorite
from part.factory import PartFactory
from webapp.models import CarBrand, CarModel, Category, Country, PriceHistory


class PartsListViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create(email="test@ex.com", password="password123")
        self.part = PartFactory.create(name="Test Part")
        self.favorite = Favorite.objects.create(user=self.user, part=self.part)

    def test_parts_list_view_authenticated_user(self):
        self.client.login(username="test@example.com", password="password123")
        response = self.client.get(reverse("part:parts_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertIn(self.part, response.context["parts"])
        self.assertIn(self.part.id, response.context["favorites"])

    def test_parts_list_view_unauthenticated_user(self):
        session_key = self.client.session.session_key
        Favorite.objects.create(session_key=session_key, part=self.part)
        response = self.client.get(reverse("part:parts_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.part.id, response.context["favorites"])


class PartsMainViewTestCase(TestCase):
    def setUp(self):
        self.part = PartFactory.create(name="Test Part")
        self.brand = CarBrand.objects.create(name="Test Brand")
        self.country = Country.objects.create(name="Test Country")
        self.model = CarModel.objects.create(name="Test Model", brand=self.brand)
        self.category = Category.objects.create(name="Test Category")
        PriceHistory.objects.create(
            part=self.part, price=100, date_changed=datetime.now()
        )

    def test_parts_main_view_search(self):
        response = self.client.get(reverse("part:parts_main") + "?search=Test")
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.part, response.context["parts"])

    def test_parts_main_view_filter(self):
        response = self.client.get(
            reverse("part:parts_main") + "?category=" + str(self.category.id)
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.part, response.context["parts"])


class PartsDetailViewTestCase(TestCase):
    def setUp(self):
        self.part = PartFactory.create(name="Test Part")
        self.related_part = PartFactory.create(
            name="Related Part", category=self.part.category
        )

    def test_parts_detail_view(self):
        response = self.client.get(
            reverse("part:part_detail", kwargs={"pk": self.part.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "part/parts_detail.html")
        self.assertIn(self.related_part, response.context["related_parts"])
