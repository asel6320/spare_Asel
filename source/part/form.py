from django import forms
from webapp.models import Country, CarBrand, CarModel, Category


class PartsFilterForm(forms.Form):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required=False, label='Страна производства')
    brand = forms.ModelChoiceField(queryset=CarBrand.objects.all(), required=False, label='Марка машины')
    model = forms.ModelChoiceField(queryset=CarModel.objects.all(), required=False, label='Модель машины')
    part_type = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Тип запчасти')
    min_price = forms.DecimalField(required=False, label="Минимальная цена", min_value=0)
    max_price = forms.DecimalField(required=False, label="Максимальная цена", min_value=0)

    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')
        if min_price and max_price and min_price > max_price:
            raise forms.ValidationError("Минимальная цена не может быть больше максимальной.")
        return cleaned_data
