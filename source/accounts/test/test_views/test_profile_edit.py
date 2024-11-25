from accounts.factory.user_factory import UserFactory
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from orders.factory import OrderPartFactory
from orders.models import Order

User = get_user_model()


class UserProfileViewTests(TestCase):

    def setUp(self):
        self.user = UserFactory.create(
            email="test@ex.com",
            password="password123",
            first_name="test",
            last_name="test",
            username="test",
        )

        self.client.login(username="test@ex.com", password="password123")
        self.profile_url = reverse("accounts:profile")
        self.cart_url = reverse("accounts:cart")

    def test_user_profile_view_authenticated(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")

    def test_user_profile_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.profile_url)
        self.assertRedirects(
            response, f"{reverse('accounts:login')}?next={self.profile_url}"
        )

    def test_profile_view_orders_context(self):
        order = Order.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            phone="123456789",
            email="john@example.com",
        )
        order_part = OrderPartFactory(
            order=order, quantity=2, name="Part A", price=10.00
        )
        response = self.client.get(self.profile_url)
        self.assertIn("orders", response.context)
        self.assertEqual(response.context["orders"].first(), order)

    def test_user_profile_form_invalid(self):
        response = self.client.post(self.profile_url, {"email": "test2@mail.ru"})
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Произошла ошибка" in str(message) for message in messages))

    def test_user_cart_view_authenticated(self):
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_cart.html")
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Корзина")

