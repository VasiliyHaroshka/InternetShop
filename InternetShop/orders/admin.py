from django.contrib import admin

from .models import OrderItem, Order


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ("product",) # field become Input


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
