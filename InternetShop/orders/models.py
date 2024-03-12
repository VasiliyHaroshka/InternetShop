from django.db import models
from shop.models import Product


class Order(models.Model):
    """Description of order"""
    first_name = models.CharField(
        "Имя",
        max_length=100,
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=100,
    )
    email = models.EmailField("Email")
    address = models.CharField(
        "Адрес",
        max_length=250,
    )
    post_index = models.CharField(
        "Почтовый индекс",
        max_length=6,
    )
    city = models.CharField(
        "Город",
        max_length=50,
    )
    created_at = models.DateTimeField(
        "Создан",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        "Отредактирован",
        auto_now=True,
    )
    paid = models.BooleanField(
        "Оплачен",
        default=False,)

    def __str__(self):
        return f"Order {self.id}, paid = {self.paid}"

    class Meta:
        ordering = ("-created_at",)
        indexes = [models.Index(fields=("-created_at",))]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def get_total_cost(self):
        """Total cost of all products in the order"""
        return sum(item.get_cost for item in self.items.all())


class OrderItem(models.Model):
    """Describe paid products and their cost"""
    order = models.ForeignKey(
        "Order",
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_items",
    )
    price = models.DecimalField(
        "Цена",
        max_digits=10,
        decimal_places=2,
    )
    count = models.PositiveIntegerField(
        "Количество",
        default=1,
    )

    def __str__(self):
        return self.id

    def get_cost(self):
        """Return cost of certain product in the order"""
        return self.price * self.count
