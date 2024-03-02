from django.db import models


class Category(models.manager):
    """Description of product's category"""
    name = models.CharField(
        "Название",
        max_length=100,
        unique=True,
    )
    slug = models.SlugField(
        "Слаг",
        max_length=100,
        unique=True,
    )

    class Meta:
        ordering = ("name",)
        indexes = (
            models.Index(fields=("name",)),
        )
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    """Description products in the internetshop"""
    name = models.CharField(
        "Название",
        max_length=100,
        unique=True,
    )
    slug = models.SlugField(
        "Слаг",
        max_length=100,
        unique=True,
    )
    image = models.ImageField(
        "Картинка",
        upload_to="products/%Y/%m/%d",
        lank=True,
    )
    description = models.TextField(
        "Описание",
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
        "Category",
        on_delete=models.CASCADE,
        verbose_name="Категория",
        related_name="category",
    )

    def __str__(self):
        return f"Товар: {self.name}"

    class Meta:
        ordering = ("name",)
        indexes = (
            models.Index(fields=("id", "slug")),
            models.Index(fields=("name",)),
            models.Index(fields=("-created_at",)),
        )
