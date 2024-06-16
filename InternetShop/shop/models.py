from django.db import models
from django.urls import reverse

from django_ckeditor_5.fields import CKEditor5Field
from parler.models import TranslatableModel, TranslatedFields


class Category(TranslatableModel):
    """Description of product's category"""
    translations = TranslatedFields(
        name=models.CharField(max_length=100),
        slug=models.SlugField(max_length=100, unique=True),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def get_absolute_url(self):
        return reverse("shop:product_list_by_category", args=[self.slug])


class Product(TranslatableModel):
    """Description products in the internetshop"""
    translations = TranslatedFields(
        name=models.CharField(max_length=100),
        slug=models.SlugField(max_length=100, unique=True),
        description=CKEditor5Field(blank=True),
    )

    image = models.ImageField(
        "Картинка",
        upload_to="products/%Y/%m/%d",
        blank=True,
    )

    price = models.DecimalField(
        "Цена",
        max_digits=10,
        decimal_places=2,
    )
    is_available = models.BooleanField(
        "Доступность",
        default=True,
    )
    created_at = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        "Дата изменения",
        auto_now=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        related_name="category",
    )

    def __str__(self):
        return f"Товар: {self.name}"

    class Meta:
        indexes = (
            models.Index(fields=("-created_at",)),
        )
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id, self.slug])
