from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase

from .admin import NewsletterAdmin
from .models import Newsletter, Subscription

User = get_user_model()


class NewsletterModelTests(TestCase):
    def test_newsletter_creation(self):
        """Тестирование создания записи Newsletter"""
        newsletter = Newsletter.objects.create(
            subject="Тестовая рассылка", body="Это тестовое сообщение."
        )
        self.assertEqual(newsletter.subject, "Тестовая рассылка")
        self.assertEqual(newsletter.body, "Это тестовое сообщение.")
        self.assertIsNotNone(newsletter.created_at)


class NewsletterAdminTests(TestCase):
    def setUp(self):
        # Создаем администратора для тестирования админки
        self.admin_user = User.objects.create_superuser(
            "admin", "admin@test.com", "password"
        )
        self.site = AdminSite()
        self.admin = NewsletterAdmin(Newsletter, self.site)

        # Создаем тестовые данные подписчиков и рассылки
        self.newsletter = Newsletter.objects.create(
            subject="Тестовая рассылка", body="Это тестовое сообщение для подписчиков."
        )
        self.active_subscriber = Subscription.objects.create(
            name="Активный пользователь", email="active@test.com", is_active=True
        )
        self.inactive_subscriber = Subscription.objects.create(
            name="Неактивный пользователь", email="inactive@test.com", is_active=False
        )

    def test_send_newsletter_to_active_subscribers(self):
        """Тест отправки рассылки только активным подписчикам"""
        queryset = Newsletter.objects.filter(id=self.newsletter.id)

        # Действие send_newsletter должно отправить письмо только активным подписчикам
        self.admin.send_newsletter(request=None, queryset=queryset)

        # Проверяем, что в почтовом ящике одно письмо
        self.assertEqual(len(mail.outbox), 1)
        # Убедимся, что письмо было отправлено на адрес активного подписчика
        self.assertIn(self.active_subscriber.email, mail.outbox[0].to)
        # Проверяем, что письмо содержит правильные данные
        self.assertEqual(mail.outbox[0].subject, "Тестовая рассылка")
        self.assertIn("Это тестовое сообщение для подписчиков.", mail.outbox[0].body)

    def test_no_email_sent_to_inactive_subscribers(self):
        """Проверка, что неактивные подписчики не получают письма"""
        queryset = Newsletter.objects.filter(id=self.newsletter.id)
        self.admin.send_newsletter(request=None, queryset=queryset)

        # Убедимся, что письмо было отправлено только активному подписчику
        self.assertNotIn(self.inactive_subscriber.email, mail.outbox[0].to)

    def test_send_newsletter_logs_error_on_failure(self):
        """Тестирование логирования при ошибке отправки письма"""
        # Устанавливаем неправильный email сервера для принудительной ошибки
        with self.settings(EMAIL_HOST_USER="invalid_email@test.com"):
            queryset = Newsletter.objects.filter(id=self.newsletter.id)

            # Действие send_newsletter с несуществующим адресом должно вызвать ошибку
            with self.assertLogs("newsletter_admin", level="ERROR") as log:
                self.admin.send_newsletter(request=None, queryset=queryset)

                # Убедимся, что ошибка была зафиксирована
                self.assertTrue(
                    any(
                        "Ошибка при отправке рассылки" in message
                        for message in log.output
                    )
                )

        # Убедимся, что письмо не было отправлено
        self.assertEqual(len(mail.outbox), 0)
