from django import forms
from .models import ContactRequest


class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ["last_name", "phone_number", "comments","email","first_name"]
        widgets = {
            "last_name": forms.TextInput(attrs={"placeholder": "Введите вашу фамилию"}),
            "phone_number": forms.TextInput(
                attrs={"placeholder": "Введите ваш номер телефона"}
            ),
            "comments": forms.TextInput(attrs={"placeholder": "Оставьте комментарии"}),
        }
        labels = {
            "last_name": "Фамилия",
            "phone_number": "Номер телефона",
            "comments": "Комментарии",
        }
