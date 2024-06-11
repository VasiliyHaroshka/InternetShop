from django.contrib import admin
from django.contrib.gis import forms
from django.utils.safestring import mark_safe

from parler.admin import TranslatableAdmin
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Product, Category


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(
        widget=CKEditorUploadingWidget(),
        label="Описание",
    )
    name = forms.CharField(
        max_length=100,
        label="Имя",
    )
    slug = forms.SlugField(
        max_length=100,
        label="Слаг",
    )

    class Meta:
        model = Product
        fields = '__all__'


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    """Registration of model 'Product' on admin panel"""
    list_display = ("name", "get_photo", "price", "category", "is_available", "created_at", "updated_at")
    list_select_related = ("category",)
    list_display_links = ('name',)
    search_fields = ('name', 'category__name')
    list_filter = ("is_available", "created_at", "updated_at")
    list_editable = ("price", "is_available")
    form = ProductAdminForm
    fields = ("name", "image", "get_photo", "slug", "price", "category", "description", "is_available")
    readonly_fields = ("get_photo", "created_at", "updated_at")
    save_on_top = True
    list_editable = ("is_available",)

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}

    def get_photo(self, item):
        if item.image:
            return mark_safe(f"<img src='{item.image.url}' width=50>")

    get_photo.short_description = "Фото товара"


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    """Registration of model 'Category' on admin panel"""
    list_display = ("name", "slug")

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}


admin.site.site_title = "Интернет магазин"
admin.site.site_header = "Интернет магазин"
