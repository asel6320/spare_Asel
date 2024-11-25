from django import forms
from django_summernote.widgets import SummernoteWidget

from webapp.models.news import News


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'full_text', 'short_description','image']
        widgets = {
            'full_text': SummernoteWidget(),
        }
