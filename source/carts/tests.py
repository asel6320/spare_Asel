from accounts.factory import UserFactory
from carts.factory import CartFactory
from carts.utils import get_user_carts
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from part.factory import PartFactory


class GetUserCartsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory(email="test@example.com", password="password123")
        self.part = PartFactory()

    def test_get_user_carts_authenticated_user(self):
        cart_item = CartFactory(user=self.user, part=self.part, quantity=1)
        request = self.factory.get("/")
        request.user = self.user
        carts = get_user_carts(request)
        self.assertIn(cart_item, carts)
        self.assertEqual(carts.count(), 1)

    def test_get_user_carts_unauthenticated_user_with_session(self):
        request = self.factory.get("/")
        request.user = AnonymousUser()
        request.session = self.client.session
        request.session.create()
        cart_item = CartFactory(
            session_key=request.session.session_key, part=self.part, quantity=1
        )
        carts = get_user_carts(request)
        self.assertIn(cart_item, carts)
        self.assertEqual(carts.count(), 1)

    def test_get_user_carts_unauthenticated_user_without_session(self):
        request = self.factory.get("/")
        request.user = AnonymousUser()
        request.session = self.client.session
        request.session.create()
        carts = get_user_carts(request)
        self.assertTrue(request.session.session_key)
        self.assertEqual(carts.count(), 0)
