from django import forms


class PriceUpdateForm(forms.Form):
    price = forms.DecimalField(
        required=False,
        decimal_places=2,
        max_digits=10,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Новая цена',
            'step': '0.01'
        }),
        label='Введите процент изменения'
    )
    percentage = forms.DecimalField(
        required=False,
        decimal_places=2,
        max_digits=10,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Процент изменения',
            'step': '0.01'
        }),
        label='Введите процент изменения'
    )

    # Поле для изменения цены до определенного значения
    price_to = forms.DecimalField(
        required=False,
        decimal_places=2,
        max_digits=10,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Сумма изменения',
            'step': '0.01'
        }),
        label='Введите сумму изменения'
    )
