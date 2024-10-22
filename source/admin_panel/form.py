from django import forms


class PriceUpdateForm(forms.Form):
    new_price = forms.DecimalField(max_digits=1000, decimal_places=2, label='Новая цена')
