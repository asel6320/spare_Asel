import re

from django import forms
from django.contrib.auth import get_user_model
from orders.models import Order
from part.models import Part
from contacts.models import ContactRequest

User = get_user_model()


class AdminOrderForm(forms.ModelForm):
    part_ids = forms.ModelMultipleChoiceField(
        queryset=Part.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True,
        label="Выбрать запчасти"
    )

    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'phone',
            'email',
            'requires_delivery',
            'delivery_address',
            'payment_on_get',
            'status',
            'part_ids'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'part_ids' in self.data:
            part_ids = self.data.getlist('part_ids')
            for part_id in part_ids:
                part = Part.objects.get(id=part_id)
                self.fields[f'quantity_{part.id}'] = forms.IntegerField(
                    min_value=1,
                    max_value=part.amount,
                    initial=1,
                    label=f"Количество для {part.name}",
                    required=True
                )

    def clean(self):
        cleaned_data = super().clean()
        part_ids = cleaned_data.get('part_ids')

        if part_ids:
            for part in part_ids:
                quantity = cleaned_data.get(f'quantity_{part.id}')

                if quantity and quantity > part.amount:
                    self.add_error(
                        f'quantity_{part.id}',
                        f'Количество не может быть больше, чем {part.amount} для детали {part.name}.'
                    )

        return cleaned_data
class CustomerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'comments']
