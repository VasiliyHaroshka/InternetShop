from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import OrderItem, Order


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ("product",)  # field become Input


def order_stripe_payment(obj: Order):
    """Return url stripe payment"""
    url = obj.get_stripe_url()
    if obj.stripe_id:
        return mark_safe(f'<a href="{url}" target="_blank">{obj.stripe_id}</a>')
    return ""


order_stripe_payment.short_description = 'Stripe payment'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id", "first_name", "last_name", "email", "address",
        "post_index", "city", "paid", "created_at", "updated_at"
    )
    list_filter = ("paid", "created_at", "updated_at")
    search_fields = ('first_name', 'last_name', "address")
    list_editable = ("first_name", "last_name", "email", "address", "post_index", "city")
    inlines = (OrderItemInline,)
