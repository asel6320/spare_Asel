from django import forms
from .models import CallbackRequest

class CallbackRequestForm(forms.ModelForm):
    class Meta:
        model = CallbackRequest
        fields = ['name', 'phone', 'comments']
