from django import forms
from django.core.exceptions import ValidationError
import re

from webapp.models import Order


class OrderForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        required_fields = ["email", "phone", "last_name", "first_name"]

        for field in required_fields:
            if not cleaned_data.get(field):
                raise ValidationError(f"Поле {field} не может быть пустым.")

        return cleaned_data

    def clean_phone_number(self):
        data = self.cleaned_data['phone']

        if not data.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры")

        pattern = re.compile(r'^\d{10}$')
        if not pattern.match(data):
            raise forms.ValidationError("Неверный формат номера")

        return data

    class Meta:
        model = Order
        fields = ["email", "phone", "last_name", "first_name", 'requires_delivery', 'delivery_address']
