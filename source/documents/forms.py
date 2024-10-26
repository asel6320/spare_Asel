from django import forms
from .models import PartDocument

class PartDocumentForm(forms.ModelForm):
    class Meta:
        model = PartDocument
        fields = ['document', 'description']
