from django.test import TestCase
from django.urls import reverse

from webapp.factory.category_factory import CategoryFactory
from webapp.factory.country_factory import CountryFactory
from webapp.factory.part_factory import PartFactory
from webapp.factory.price_history_factory import PriceHistoryFactory


class TestPart(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = CategoryFactory(name="Engine Parts")
        cls.part = PartFactory(name="Part 1", category=cls.category)
        cls.related_part1 = PartFactory(name="related part1", category=cls.category)
        cls.related_part2 = PartFactory(name="related part2", category=cls.category)
        cls.unrelated_part = PartFactory(
            name="related part3", category=CategoryFactory(name="bb")
        )
        cls.country = CountryFactory(name="USA")
        cls.another_country = CountryFactory(name="Germany")

    def setUp(self):
        self.part1 = PartFactory(vehicle_info__countries=[self.country])
        self.part2 = PartFactory(vehicle_info__countries=[self.country])
        self.unrelated_part = PartFactory(
            vehicle_info__countries=[self.another_country]
        )
        self.price1 = PriceHistoryFactory(part=self.part1, price=200.00)
        self.price2 = PriceHistoryFactory(part=self.part2, price=100.00)
        self.price_unrelated = PriceHistoryFactory(
            part=self.unrelated_part, price=300.00
        )

    def test_about_us_template(self):
        response = self.client.get(reverse("webapp:about_us"))
        self.assertTemplateUsed(response, template_name="part/about_us.html")

    def test_get_context_data_contains_related_parts(self):
        response = self.client.get(
            reverse("webapp:part_detail", kwargs={"pk": self.part.pk})
        )
        self.assertEqual(response.status_code, 200)
        related_parts = response.context["related_parts"]
        self.assertEqual(len(related_parts), 2)
        self.assertIn(self.related_part1, related_parts)
        self.assertIn(self.related_part2, related_parts)
        self.assertNotIn(self.unrelated_part, related_parts)

    def test_get_context_data_contains_category(self):
        response = self.client.get(
            reverse("webapp:part_detail", kwargs={"pk": self.part.pk})
        )
        category = response.context["category"]
        self.assertEqual(category, self.part.category)
