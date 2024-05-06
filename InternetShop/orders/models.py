from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from coupons.models import Coupon
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
        default=False,
    )
    stripe_id = models.CharField(
        "Идентификатор связанного платежа",
        max_length=250,
        blank=True,
    )
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name="Купон",
    )
    discount = models.IntegerField(
        "Процент скидки",
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )

    def __str__(self):
        return f"Order {self.id}, paid = {self.paid}"

    class Meta:
        ordering = ("-created_at",)
        indexes = [models.Index(fields=("-created_at",))]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def get_total_cost_before_discount(self):
        """Итоговая стоимость заказа без скидки"""
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        """Применение скидки к заказу"""
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)

    def get_total_cost(self):
        """Total cost of all products in the order with discount (if it is)"""
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()

    def get_stripe_url(self):
        """Получение ссылки на каждый id платежа в информационной панели stripe"""
        if not self.stripe_id:
            return ""
        if "_test_" in settings.STRIPE_SECRET_KEY:
            path = "/test/"
        else:
            path = "/"
        return f"https://dashboard.stripe.com{path}payments/{self.stripe_id}"


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
    quantity = models.PositiveIntegerField(
        "Количество",
        default=1,
    )

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        """Return cost of certain product in the order"""
        return self.price * self.quantity
