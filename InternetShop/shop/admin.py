from django.contrib import admin

from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Registration of model 'Product' on admin panel"""
    list_display = ("name", "slug", "price", "category", "is_available", "created_at", "updated_at")
    list_select_related = ("category",)
    list_display_links = ('name',)
    search_fields = ('name', 'category__name',)
    list_filter = ("is_available", "created_at", "updated_at")
    list_editable = ("price", "is_available")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Registration of model 'Category' on admin panel"""
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
