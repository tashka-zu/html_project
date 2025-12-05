from django import forms
from django.core.exceptions import ValidationError
from .models import Product

class ProductForm(forms.ModelForm):
    forbidden_words = [
        'казино', 'криптовалюта', 'крипта', 'биржа',
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        name = self.cleaned_data['name']
        for word in self.forbidden_words:
            if word in name.lower():
                raise ValidationError(f"Название не должно содержать запрещенное слово: {word}.")
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        for word in self.forbidden_words:
            if word in description.lower():
                raise ValidationError(f"Описание не должно содержать запрещенное слово: {word}.")
        return description

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        return price
