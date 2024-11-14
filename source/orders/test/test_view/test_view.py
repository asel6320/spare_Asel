from accounts.factory import UserFactory
from carts.models import Cart
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from orders.models import Order
from part.factory import PartFactory
from webapp.factory.price_history_factory import PriceHistoryFactory


class OrderCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create(email="test@example.com", password="password123")
        self.part = PartFactory(amount=5)
        PriceHistoryFactory(part=self.part, price=100)
        self.order_url = reverse("order:order_create")

    def test_order_create_view_with_cart_items(self):
        self.client.login(username="test@example.com", password="password123")
        Cart.objects.create(user=self.user, part=self.part, quantity=3)

        response = self.client.post(
            self.order_url,
            {
                "first_name": "Test",
                "last_name": "User",
                "email": "test@example.com",
                "phone": "1234567890",
                "delivery_address": "123 Test St",
                "requires_delivery": "1",
                "payment_on_get": "1",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Order.objects.filter(user=self.user).exists())
        order = Order.objects.first()
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.first_name, "Test")
        self.assertFalse(Cart.objects.filter(user=self.user).exists())

    def test_order_create_view_with_empty_cart(self):
        self.client.login(username="test@example.com", password="password123")

        response = self.client.post(
            self.order_url,
            {
                "first_name": "Test",
                "last_name": "User",
                "email": "test@example.com",
                "phone": "1234567890",
                "requires_delivery": "1",
                "delivery_address": "123 Test St",
                "payment_on_get": "1",
            },
        )

        self.assertEqual(response.status_code, 302)
        storage = get_messages(response.wsgi_request)
        messages = [message.message for message in storage]
        self.assertIn("Невозможно оформить заказ: корзина пуста.", messages)

    def test_order_create_view_with_insufficient_stock(self):
        self.client.login(username="test@example.com", password="password123")
        Cart.objects.create(user=self.user, part=self.part, quantity=10)

        response = self.client.post(
            self.order_url,
            {
                "first_name": "Test",
                "last_name": "User",
                "email": "test@example.com",
                "phone": "1234567890",
                "requires_delivery": "1",
                "delivery_address": "123 Test St",
                "payment_on_get": "1",
            },
        )

        storage = get_messages(response.wsgi_request)
        messages = [message.message for message in storage]
        self.assertTrue(
            any("Недостаточное количество товара" in message for message in messages),
            f"Expected message not found. Messages: {messages}",
        )

    def test_order_create_view_invalid_form(self):
        self.client.login(username="test@example.com", password="password123")
        Cart.objects.create(user=self.user, part=self.part, quantity=2)

        response = self.client.post(
            self.order_url,
            {
                "first_name": "Test",
                "email": "test@example.com",
                "phone": "1234567890",
                "requires_delivery": "1",
                "delivery_address": "123 Test St",
                "payment_on_get": "1",
            },
        )

        self.assertEqual(response.status_code, 200)
        storage = get_messages(response.wsgi_request)
        messages = [message.message for message in storage]
        self.assertIn("Заполните все обязательные поля!", messages)
