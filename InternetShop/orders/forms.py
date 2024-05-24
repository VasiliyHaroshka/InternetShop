from django import forms

from localflavor.ru.forms import RUPostalCodeField

from .models import Order


class OrderForm(forms.ModelForm):
    """Form of order creation"""
    post_code = RUPostalCodeField()

    class Meta:
        model = Order
        fields = (
            "first_name", "last_name", "email",
            "city", "address", "post_code",
        )
