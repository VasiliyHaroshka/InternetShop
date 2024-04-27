from django import forms


class CouponApplyForm(forms.Form):
    """Coupon form"""
    code = forms.CharField(max_length=50)
