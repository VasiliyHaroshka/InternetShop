from django.contrib import admin

from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """Add model Coupon to admin panel with some settings"""
    list_display = (
        "code", "valid_from", "valid_to", "discount", "is_active"
    )
    list_filter = (
        "valid_from", "valid_to", "is_active"
    )
    search_fields = (
        "code",
    )
