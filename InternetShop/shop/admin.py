from django.contrib import admin

from parler.admin import TranslatableAdmin

from .models import Product, Category


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    """Registration of model 'Product' on admin panel"""
    list_display = ("name", "slug", "price", "category", "is_available", "created_at", "updated_at")
    list_select_related = ("category",)
    list_display_links = ('name',)
    search_fields = ('name', 'category__name')
    list_filter = ("is_available", "created_at", "updated_at")
    list_editable = ("price", "is_available")

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    """Registration of model 'Category' on admin panel"""
    list_display = ("name", "slug")

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}
