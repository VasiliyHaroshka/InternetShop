import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import OrderItem, Order


def order_pdf(obj):
    """Add link to pdf-report for every order"""
    url = reverse("orders:admin_order_pdf", args=[obj.id])
    return mark_safe(f"<a href='{url}'>PDF</a>")


order_pdf.short_description = "Invoice"


def export_to_csv(modeladmin, request, queryset):
    """Create action 'export to csv' for admin panel"""
    opts = modeladmin.model._meta
    content_disposition = f"attachment; filename={opts.verbose_name}.csv"
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = content_disposition

    writer = csv.writer(response)
    fields = [
        field
        for field in opts.get_fields()
        if
        not field.many_to_many
        and
        not field.one_to_many
    ]
    writer.writerow([field.verbose_name for field in fields])  # заголовки

    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%d/%m/%Y")
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = "Export to CSV"


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


def order_detail(obj: Order):
    url = reverse("orders:admin_order_detail", args=[obj.id])
    return mark_safe(f"<a href='{url}'>View</a>")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Add model Order to admin panel with some settings"""
    list_display = (
        "id", "first_name", "last_name", "email", "address",
        "post_index", "city", "paid", "created_at", "updated_at",
        order_detail, order_pdf,
    )
    list_filter = ("paid", "created_at", "updated_at")
    search_fields = ('first_name', 'last_name', "address")
    list_editable = ("first_name", "last_name", "email", "address", "post_index", "city")
    inlines = (OrderItemInline,)
    actions = (export_to_csv,)
