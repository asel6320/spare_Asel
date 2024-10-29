from django.test import TestCase
from django.urls import reverse
from webapp.factory.part_factory import PartFactory
from webapp.factory.cart_factory import CartFactory

from accounts.factory.user_factory import UserFactory
from webapp.factory.price_history_factory import PriceHistoryFactory
from carts.models import Cart


class TestCart(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create(
            password="password", username="testuser", phone_number="123456789"
        )

    def setUp(self):
        self.part = PartFactory(amount=10)
        self.cart = CartFactory(part=self.part, user=self.user, quantity=2)
        self.price_history = PriceHistoryFactory(part=self.part, price=100.00)

    def test_add_part_to_cart_authenticated(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("webapp:part_add_cart", kwargs={"pk": self.part.pk})
        )
        self.assertRedirects(response, reverse("webapp:parts_list"))
        cart_item = Cart.objects.get(user=self.user, part=self.part)
        self.assertEqual(cart_item.quantity, 3)

    def test_add_part_to_cart_not_authenticated(self):
        response = self.client.post(
            reverse("webapp:part_add_cart", kwargs={"pk": self.part.pk})
        )
        self.assertRedirects(response, reverse("webapp:parts_list"))
        session_key = self.client.session.session_key
        cart_item = Cart.objects.get(session_key=session_key, part=self.part)
        self.assertEqual(cart_item.quantity, 1)

    def test_add_part_exceeds_amount(self):
        self.client.login(username="testuser", password="password")
        for _ in range(10):
            self.client.post(
                reverse("webapp:part_add_cart", kwargs={"pk": self.part.pk})
            )
        cart_item = Cart.objects.get(user=self.user, part=self.part)
        self.assertEqual(cart_item.quantity, 10)

    def test_add_part_when_not_available(self):
        self.part.amount = 0
        self.part.save()
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("webapp:part_add_cart", kwargs={"pk": self.part.pk})
        )
        self.assertRedirects(response, reverse("webapp:parts_list"))
        cart_items = Cart.objects.filter(user=self.user, part=self.part)
        self.assertEqual(cart_items.count(), 1)

    def test_delete_cart_item_quantity_greater_than_one(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("webapp:cart_delete", kwargs={"pk": self.cart.pk})
        )
        self.assertRedirects(response, reverse("webapp:cart"))
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.quantity, 1)

    def test_delete_cart_item_quantity_equal_to_one(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("webapp:cart_delete", kwargs={"pk": self.cart.pk})
        )
        self.assertRedirects(response, reverse("webapp:cart"))
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.quantity, 1)

    def test_delete_cart_item_non_auth(self):
        self.cart.quantity = 1
        self.cart.save()

        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("webapp:cart_delete", kwargs={"pk": self.cart.pk})
        )
        self.assertRedirects(response, reverse("webapp:cart"))
        self.assertEqual(self.cart.quantity, 1)
        with self.assertRaises(Cart.DoesNotExist):
            self.cart.refresh_from_db()
