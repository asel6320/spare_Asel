from django import forms
from orders.models import Order  # Adjust the import according to your models

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'requires_delivery', 'delivery_address', 'payment_on_get']  # Add any other fields needed
        widgets = {
            'delivery_address': forms.TextInput(attrs={'placeholder': 'Введите адрес доставки'}),
            # Customize widgets as needed
        }

