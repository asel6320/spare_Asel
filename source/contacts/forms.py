from django import forms
from .models import ContactRequest


class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ["last_name", "phone_number", "comments","first_name","email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Введите ваше имя"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Введите вашу фамилию"}),
            "phone_number": forms.TextInput(
                attrs={"placeholder": "Введите ваш номер телефона"}
            ),
            "email": forms.EmailInput(attrs={"placeholder": "Введите ваш email"}),
            "comments": forms.TextInput(attrs={"placeholder": "Оставьте комментарии"}),
        }
        labels = {
            "first_name":"Имя",
            "last_name": "Фамилия",
            "phone_number": "Номер телефона",
            "email":"Email",
            "comments": "Комментарии",
        }
