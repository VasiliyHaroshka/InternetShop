from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    """Form of order creation"""
    class Meta:
        model = Order
        fields = (
            "first_name", "last_name", "email",
            "address", "post_index", "city",
        )