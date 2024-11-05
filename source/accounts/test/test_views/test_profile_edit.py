from accounts.factory.user_factory import UserFactory
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class TestUserProfileView(TestCase):

    def setUp(self):
        self.user = UserFactory.create(password="password")
        self.client.login(username=self.user.username, password="password")
        self.profile_url = reverse(
            "accounts:profile"
        )  # Убедитесь, что здесь правильное имя URL

    def test_profile_update_valid(self):
        # Создание данных для обновления профиля
        form_data = {
            "first_name": "UpdatedFirstName",
            "last_name": "UpdatedLastName",
            "email": "updated@example.com",
            # добавьте другие поля формы, если есть
        }
        response = self.client.post(self.profile_url, data=form_data)

        # Проверьте, что ответ перенаправляет на нужный URL
        self.assertRedirects(response, self.profile_url)

        # Проверьте, что профиль обновлен в базе данных
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "UpdatedFirstName")
        self.assertEqual(self.user.last_name, "UpdatedLastName")
        self.assertEqual(self.user.email, "updated@example.com")

        # Проверьте наличие сообщения об успешном обновлении профиля
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, "Профайл успешно обновлен")

    def test_profile_update_invalid(self):
        # Создание данных для обновления профиля с ошибками
        form_data = {
            "first_name": "",  # Пустое имя должно вызвать ошибку валидации
            "last_name": "UpdatedLastName",
            "email": "invalid_email",  # Неверный email
            # добавьте другие поля формы, если есть
        }
        response = self.client.post(self.profile_url, data=form_data)

        # Проверьте, что ответ не перенаправляет (это ошибка формы)
        self.assertEqual(response.status_code, 200)

        # Проверьте наличие сообщения об ошибке
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, "Произошла ошибка")


class TestUserCartView(TestCase):

    def setUp(self):
        self.user = UserFactory.create(password="password")
        self.client.login(username=self.user.username, password="password")
        self.cart_url = reverse(
            "accounts:cart"
        )  # Убедитесь, что здесь правильное имя URL

    def test_user_cart_view(self):
        response = self.client.get(self.cart_url)

        # Проверьте, что ответ успешен и отображается правильный шаблон
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_cart.html")

        # Проверьте, что контекст содержит правильные данные
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Корзина")
