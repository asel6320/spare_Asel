from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from webapp.models import CarBrand


class AdminPanelTests(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(
            username="admin_test",
            is_staff=True,
            is_active=True,
            phone_number="1",
            email="admin@1.com",
            first_name="Admin",
            last_name="Test",
        )
        self.user.set_password("testpass123")
        self.user.save()
        print(f"Пользователь создан: {self.user.username}")
        user = get_user_model().objects.get(username="admin_test")
        print(f"Username: {self.user.username}, Password: 'testpass123'")
        print(f"Check password: {self.user.check_password('testpass123')}")
        print(user.check_password("testpass123"))

    def login_staff_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("admin_panel:admin_home"))
        print(f"Код ответа: {response.status_code}")
        self.assertEqual(response.status_code, 200)

    def test_admin_home_access_for_staff(self):
        """Тест: доступ к главной странице только для пользователей is_staff."""
        self.login_staff_user()
        response = self.client.get(reverse("admin_panel:admin_home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_admin_home_access_for_non_staff(self):
        """Тест: редирект для неавторизованных или non-staff пользователей."""
        response = self.client.get(reverse("admin_panel:admin_home"))
        self.assertEqual(response.status_code, 302)

    def test_create_car_brand(self):
        """Тест: создание новой марки автомобиля."""
        self.login_staff_user()
        response = self.client.post(
            reverse("admin_panel:model_add", args=["carbrand"]), {"name": "Toyota2"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CarBrand.objects.filter(name="Toyota2").exists())

    def test_edit_car_brand(self):
        """Тест: редактирование существующей марки автомобиля."""
        self.login_staff_user()
        car_brand = CarBrand.objects.create(name="Honda")
        response = self.client.post(
            reverse("admin_panel:model_edit", args=["carbrand", car_brand.id]),
            {"name": "Honda Updated"},
        )
        self.assertEqual(response.status_code, 302)
        car_brand.refresh_from_db()  # Обновляем объект из базы
        self.assertEqual(car_brand.name, "Honda Updated")

    def test_delete_car_brand(self):
        """Тест: удаление существующей марки автомобиля."""
        self.login_staff_user()
        car_brand = CarBrand.objects.create(name="Ford")
        response = self.client.post(
            reverse("admin_panel:model_delete", args=["carbrand", car_brand.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CarBrand.objects.filter(id=car_brand.id).exists())
