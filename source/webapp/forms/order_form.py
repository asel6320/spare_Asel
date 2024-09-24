from django import forms
from django.core.exceptions import ValidationError

from webapp.models import Order


class OrderForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        required_fields = ["email", "phone", "last_name", "first_name"]

        for field in required_fields:
            if not cleaned_data.get(field):
                raise ValidationError(f"Поле {field} не может быть пустым.")

        return cleaned_data

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Ваша фамилия'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Ваш номер телефона'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ваш email'}),
        }
