from accounts.factory import UserFactory
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from favorite.factory import FavoriteFactory
from favorite.utils import get_favorite
from part.factory import PartFactory


class GetUserFavoriteTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory(email="test@example.com", password="password123")
        self.part = PartFactory()

    def test_get_user_carts_authenticated_user(self):
        favorite_item = FavoriteFactory(user=self.user, part=self.part)
        request = self.factory.get("/")
        request.user = self.user
        favorites = get_favorite(request)
        self.assertIn(favorite_item, favorites)
        self.assertEqual(favorites.count(), 1)

    def test_get_user_carts_unauthenticated_user_with_session(self):
        request = self.factory.get("/")
        request.user = AnonymousUser()
        request.session = self.client.session
        request.session.create()
        favorite_item = FavoriteFactory(
            session_key=request.session.session_key, part=self.part
        )
        favorites = get_favorite(request)
        self.assertIn(favorite_item, favorites)

    def test_get_user_carts_unauthenticated_user_without_session(self):
        request = self.factory.get("/")
        request.user = AnonymousUser()
        request.session = self.client.session
        request.session.create()
        favorites = get_favorite(request)
        self.assertTrue(request.session.session_key)
        self.assertEqual(favorites.count(), 0)
