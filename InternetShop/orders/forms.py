from django import forms

from localflavor.ru.forms import RUPostalCodeField
from captcha.fields import CaptchaField

from .models import Order


class OrderForm(forms.ModelForm):
    """Form of order creation"""
    post_index = RUPostalCodeField()
    captcha = CaptchaField()

    class Meta:
        model = Order
        fields = (
            "first_name", "last_name", "email",
            "city", "address", "post_index",
        )
