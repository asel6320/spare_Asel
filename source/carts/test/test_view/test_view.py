from accounts.factory import UserFactory
from carts.models import Cart
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from part.factory import PartFactory
from webapp.factory.price_history_factory import PriceHistoryFactory

User = get_user_model()


class CartViewsTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create(email="test@example.com", password="password123")
        self.part = PartFactory()
        PriceHistoryFactory(part=self.part, price=100)

    def test_cart_add_view(self):
        self.client.login(username="test@example.com", password="password123")
        response = self.client.post(
            reverse("cart:cart_add"),
            {"part_id": self.part.id},
            HTTP_REFERER=reverse("order:order_create"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Товар добавлен в корзину", response.json()["message"])

        cart_item = Cart.objects.get(part=self.part, user=self.user)
        self.assertEqual(cart_item.quantity, 1)

    def test_cart_change_view(self):
        self.client.login(username="test@example.com", password="password123")
        cart_item = Cart.objects.create(user=self.user, part=self.part, quantity=1)

        response = self.client.post(
            reverse("cart:cart_change"),
            {"cart_id": cart_item.id, "quantity": 3},
            HTTP_REFERER=reverse("order:order_create"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Количество изменено", response.json()["message"])

        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 3)

    def test_cart_delete_view(self):
        self.client.login(username="test@example.com", password="password123")
        cart_item = Cart.objects.create(user=self.user, part=self.part, quantity=1)

        response = self.client.post(
            reverse("cart:cart_delete"),
            {"cart_id": cart_item.id},
            HTTP_REFERER=reverse("order:order_create"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Товар удален из корзины", response.json()["message"])

        with self.assertRaises(Cart.DoesNotExist):
            Cart.objects.get(id=cart_item.id)
