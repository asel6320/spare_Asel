from django import forms

from webapp.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Введите ваш отзыв',
                'class': 'form-control rounded-3',
                'style': 'resize: none;',
            }),
        }

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text:
            raise forms.ValidationError('Отзыв не может быть пустым')
        return text
