import re

from django import forms
from django.contrib.auth import get_user_model
from orders.models import Order
from part.models import Part

User = get_user_model()


class AdminOrderForm(forms.ModelForm):
    part_ids = forms.ModelMultipleChoiceField(
        queryset=Part.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Выбрать запчасти",
    )

    class Meta:
        model = Order
        fields = [
            "first_name",
            "last_name",
            "phone",
            "email",
            "requires_delivery",
            "delivery_address",
            "payment_on_get",
            "status",
            "part_ids",
        ]


class CustomerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
        ]  # Include the fields you want to edit
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
        }
