from accounts.factory import UserFactory
from carts.models import Cart
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from orders.models import Order, OrderPart
from part.factory import PartFactory
from webapp.factory.price_history_factory import PriceHistoryFactory

User = get_user_model()


class OrderCreateViewTests(TestCase):
    def setUp(self):
        self.user = UserFactory.create(email="test@example.com", password="password")
        self.part = PartFactory()
        PriceHistoryFactory(part=self.part, price=100)
        self.cart_item = Cart.objects.create(user=self.user, part=self.part, quantity=2)
        self.url = reverse("order:order_create")

    def test_order_creation_success(self):
        self.client.login(username="test@example.com", password="password")
        response = self.client.post(
            self.url,
            {
                "first_name": "John",
                "last_name": "Doe",
                "phone": "1234567890",
                "email": "john@example.com",
                "delivery_address": "123 Test St",
                "payment_on_get": "1",
            },
        )
        self.assertRedirects(response, reverse("part:parts_list"))

        order = Order.objects.get(user=self.user)
        order_part = OrderPart.objects.get(order=order, part=self.part)

        # Проверяем данные заказа
        self.assertEqual(order.first_name, "John")
        self.assertEqual(order.last_name, "Doe")
        self.assertEqual(order_part.quantity, 2)

        # Проверяем, что товар вычтен из остатков
        self.part.refresh_from_db()
        self.assertEqual(self.part.amount, 8)

        # Проверяем, что корзина очищена
        self.assertFalse(Cart.objects.filter(user=self.user).exists())

    def test_empty_cart(self):
        """Test ordering with an empty cart."""
        Cart.objects.filter(user=self.user).delete()
        self.client.login(username="test@example.com", password="password")
        response = self.client.post(
            self.url,
            {
                "first_name": "John",
                "last_name": "Doe",
                "phone": "1234567890",
                "email": "john@example.com",
                "delivery_address": "123 Test St",
                "payment_on_get": "1",
            },
        )

        # Проверка, что отображается ошибка
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Заполните все обязательные поля!", str(messages[-1]))

    def test_insufficient_stock(self):
        """Test handling insufficient stock for an item."""
        self.part.amount = 1
        self.part.save()
        self.client.login(username="test@example.com", password="password")

        response = self.client.post(
            self.url,
            {
                "first_name": "John",
                "last_name": "Doe",
                "phone": "1234567890",
                "email": "john@example.com",
                "delivery_address": "123 Test St",
                "payment_on_get": "1",
            },
        )

        # Проверка, что появляется сообщение об ошибке
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Недостаточное количество товара", str(messages[-1]))

        # Проверка, что заказ не был создан
        self.assertFalse(Order.objects.filter(user=self.user).exists())

    def test_autofill_initial_data_for_authenticated_user(self):
        """Test that authenticated user's information is autofilled."""
        self.client.login(username="test@example.com", password="password")
        response = self.client.get(self.url)

        form = response.context["form"]
        self.assertEqual(form.initial["first_name"], self.user.first_name)
        self.assertEqual(form.initial["last_name"], self.user.last_name)
        self.assertEqual(form.initial["email"], self.user.email)

    def test_cart_cleared_after_order(self):
        """Test that the cart is cleared after a successful order."""
        self.client.login(username="test@example.com", password="password")
        self.client.post(
            self.url,
            {
                "first_name": "John",
                "last_name": "Doe",
                "phone": "1234567890",
                "email": "john@example.com",
                "delivery_address": "123 Test St",
                "payment_on_get": "1",
            },
        )

        # Проверка, что корзина очищена
        self.assertFalse(Cart.objects.filter(user=self.user).exists())
