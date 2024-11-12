from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.messages import get_messages
from .models import Subscription
from .forms import SubscriptionForm
from .views import send_confirmation_email


class SubscriptionModelTest(TestCase):
    def test_create_subscription(self):
        subscription = Subscription.objects.create(name="John Doe", email="john@example.com")
        self.assertEqual(subscription.name, "John Doe")
        self.assertEqual(subscription.email, "john@example.com")
        self.assertTrue(subscription.is_active)

    def test_unique_email(self):
        Subscription.objects.create(name="John Doe", email="john@example.com")
        with self.assertRaises(Exception):
            Subscription.objects.create(name="Jane Doe", email="john@example.com")


class SubscriptionViewTest(TestCase):
    def setUp(self):
        self.url = reverse("newsletter:subscribe")

    def test_get_subscription_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], SubscriptionForm)

    def test_successful_subscription(self):
        response = self.client.post(self.url, {"name": "John Doe", "email": "john@example.com"})
        self.assertRedirects(response, reverse("part:parts_list"))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(messages[0].message, "Вы успешно подписались на рассылку!")
        self.assertEqual(Subscription.objects.count(), 1)

    def test_duplicate_email_subscription(self):
        Subscription.objects.create(name="John Doe", email="john@example.com")
        response = self.client.post(self.url, {"name": "Jane Doe", "email": "john@example.com"})
        self.assertRedirects(response, reverse("part:parts_list"))
        self.assertEqual(Subscription.objects.count(), 1)

        messages = list(get_messages(response.wsgi_request))
        self.assertGreater(len(messages), 0)
        self.assertEqual(messages[0].message, "Вы уже подписаны на рассылку!")
        self.assertEqual(messages[0].level_tag, "warning") 


class SendConfirmationEmailTest(TestCase):
    def test_send_confirmation_email(self):
        from .views import send_confirmation_email

        send_confirmation_email("John Doe", "john@example.com")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Подтверждение подписки")
        self.assertIn("Здравствуйте, John Doe!", mail.outbox[0].body)
        self.assertEqual(mail.outbox[0].to, ["john@example.com"])

    def test_send_email_timeout(self):
        with self.assertRaises(Exception):
            with self.settings(EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"):
                send_confirmation_email("John Doe", "invalid_email@example.com")


class SubscriptionFormTest(TestCase):
    def test_form_valid_data(self):
        form = SubscriptionForm(data={
            "name": "User test",
            "email": "john@example.com"
        })
        self.assertTrue(form.is_valid())

    def test_form_empty_data(self):
        form = SubscriptionForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("email", form.errors)

    def test_form_invalid_email(self):
        form = SubscriptionForm(data={
            "name": "User test",
            "email": "invalid-email"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_form_duplicate_email(self):
        Subscription.objects.create(name="Existing User", email="duplicate@example.com")
        form = SubscriptionForm(data={
            "name": "New User",
            "email": "duplicate@example.com"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

