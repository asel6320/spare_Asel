from django.test import TestCase
from django.urls import reverse
from webapp.factory.cart_factory import CartFactory

from accounts.factory.user_factory import UserFactory
from webapp.factory.order_factory import OrderFactory
from orders.form import OrderForm
from orders.models import Order, OrderPart
from carts.models import Cart


class TestOrder(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create(password='password', username='testuser', phone_number='123456789')

    def setUp(self):
        self.order = OrderFactory(first_name='Beka', last_name='mmmm')
        self.cart = CartFactory(user=self.user, quantity=2)
        self.client.login(username=self.user.username, password='password')
        self.url = reverse('webapp:order_create')

    def test_order_create_view_get_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/user_cart.html')
        self.assertIn('order_form', response.context)
        form = response.context['order_form']
        self.assertIsInstance(form, OrderForm)
        self.assertEqual(form.fields['first_name'].initial, self.user.first_name)
        self.assertEqual(form.fields['last_name'].initial, self.user.last_name)
        self.assertEqual(form.fields['phone'].initial, self.user.phone_number)
        self.assertEqual(form.fields['email'].initial, self.user.email)

    def test_order_create_view_get_anonymous_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/user_cart.html')
        form = response.context['order_form']
        self.assertIsInstance(form, OrderForm)
        self.assertNotIn('first_name', form.initial)

    def test_order_create_view_post_valid_form(self):
        form_data = {
            'first_name': 'beka',
            'last_name': 'mus',
            'phone': '123456789',
            'email': 'beka@example.com',
        }
        response = self.client.post(self.url, data=form_data)
        self.assertTrue(Order.objects.filter(user=self.user).exists())
        order = Order.objects.get(user=self.user)
        self.assertEqual(OrderPart.objects.filter(order=order).count(), 1)
        order_part = OrderPart.objects.get(order=order)
        self.assertEqual(order_part.part, self.cart.part)
        self.assertEqual(order_part.quantity, self.cart.quantity)
        self.assertFalse(Cart.objects.filter(user=self.user).exists())
        self.assertRedirects(response, reverse('webapp:parts_list'))

    def test_order_create_view_post_invalid_form(self):
        form_data = {
            'first_name': '',
            'last_name': 'mus',
            'phone': '123456789',
            'email': 'beka@example.com',
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/user_cart.html')
        self.assertFalse(Order.objects.filter(user=self.user).exists())


