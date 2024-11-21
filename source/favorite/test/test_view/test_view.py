from accounts.factory import UserFactory
from django.test import TestCase
from django.urls import reverse
from favorite.models import Favorite
from part.factory import PartFactory


class FavoriteViewsTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create(email="test@ex.com", password="password123")
        self.part = PartFactory.create(amount=5)
        self.part1 = PartFactory.create(amount=5)
        self.part2 = PartFactory.create(amount=5)
        self.favorite_item1 = Favorite.objects.create(user=self.user, part=self.part1)
        self.favorite_item2 = Favorite.objects.create(user=self.user, part=self.part2)


    def test_user_favorite_view(self):
        self.client.login(username="test@ex.com", password="password123")
        response = self.client.get(reverse("favorite:favorite_template"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.part1.name)
        self.assertContains(response, self.part2.name)

    def test_favorite_add_view(self):
        self.client.login(username="test@ex.com", password="password123")
        response = self.client.post(
            reverse("favorite:favorite_add"),
            {"part_id": self.part.id},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Товар добавлен в избранное", response.json()["message"])

        favorite_item = Favorite.objects.get(user=self.user, part=self.part)
        self.assertEqual(favorite_item.part, self.part)

    def test_favorite_add_view_with_nonexistent_part(self):
        self.client.login(username="test@ex.com", password="password123")
        response = self.client.post(
            reverse("favorite:favorite_add"),
            {"part_id": 9999},
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("Товар не найден", response.json()["message"])

    def test_favorite_add_view_unauthenticated(self):
        response = self.client.post(
            reverse("favorite:favorite_add"),
            {"part_id": self.part.id},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Товар добавлен в избранное", response.json()["message"])
        favorite_item = Favorite.objects.get(
            session_key=self.client.session.session_key, part=self.part
        )
        self.assertEqual(favorite_item.part, self.part)

    def test_favorite_delete_view(self):
        self.client.login(username="test@ex.com", password="password123")
        response = self.client.post(
            reverse("favorite:favorite_delete"),
            {"favorite_id": self.favorite_item1.id},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Товар удалён из избранного", response.json()["message"])

        with self.assertRaises(Favorite.DoesNotExist):
            Favorite.objects.get(id=self.favorite_item1.id)
