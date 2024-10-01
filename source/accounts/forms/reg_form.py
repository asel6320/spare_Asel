from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User

class RegisterForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True, help_text='Обязательно для заполнения')

    class Meta:
        model = User
        fields = ['email', 'username', 'phone_number', 'password1', 'password2']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Пользователь с этим номером телефона уже зарегистрирован.")
        return phone_number