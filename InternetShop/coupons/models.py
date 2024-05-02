from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Coupon(models.Model):
    """Model of discount coupon"""
    code = models.CharField(
        "Код",
        max_length=50,
        unique=True
    )
    valid_from = models.DateTimeField("Действителен с")
    valid_to = models.DateTimeField("Действителен по")
    discount = models.IntegerField(
        "Процент скидки",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        help_text="Percentage value (0 to 100)"
    )
    is_active = models.BooleanField("Активен", default=False)

    def __str__(self):
        return self.code
