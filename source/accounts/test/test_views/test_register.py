from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.sessions.middleware import SessionMiddleware
from accounts.factory.user_factory import UserFactory
from carts.factory import CartFactory
from carts.models import Cart
from accounts.forms.registration import RegisterForm


class TestRegister(TestCase):

    def setUp(self):
        # Create a user using the factory
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

    def test_get_register_view(self):
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")
        self.assertIsInstance(response.context["form"], RegisterForm)

    def test_post_register_view_success(self):
        # Simulate a user registration via POST
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "user2",
                "password1": "password2",
                "password2": "password2",
                "phone_number": "1234567890",
            },
        )

        # Check if the user was redirected to the success URL
        self.assertRedirects(response, reverse("part:parts_list"))

        # Check that the user was successfully created
        user = get_user_model().objects.get(username="user2")
        self.assertIsNotNone(user)

        # Check if the user was logged in
        user_logged_in = self.client.session.get("_auth_user_id")
        self.assertEqual(str(user_logged_in), str(user.pk))

        # Check the success message in the response
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].message, f"{user.username} - вы успешно зарегистрировались")

        # Ensure that the cart is associated with the new user
        session_key = self.client.session.session_key
        cart = Cart.objects.filter(session_key=session_key).first()
        self.assertEqual(cart.user, user)

    def test_post_register_view_invalid(self):
        # Simulate an invalid registration with missing fields or mismatched passwords
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "user2",
                "password1": "password2",
                "password2": "password3",  # Passwords don't match
                "phone_number": "1234567890",
            },
        )

        # Check that the form contains errors and the user is not redirected
        self.assertFormError(response, "form", "password2", "The two password fields didn’t match.")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_post_register_view_existing_cart(self):
        # Simulate a session with a cart
        session = self.client.session
        session.create()  # Ensure session key is created
        session_key = session.session_key
        cart = CartFactory(session_key=session_key)

        # Simulate a user registration via POST
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "user2",
                "password1": "password2",
                "password2": "password2",
                "phone_number": "1234567890",
            },
        )

        # Check that the user's cart is associated
        user = get_user_model().objects.get(username="user2")
        cart.refresh_from_db()  # Refresh the cart from the database
        self.assertEqual(cart.user, user)
