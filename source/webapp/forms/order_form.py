from django import forms

from webapp.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Ваша фамилия'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Ваш номер телефона'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ваш email'}),
        }