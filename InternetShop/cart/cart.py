from decimal import Decimal

from django.conf import settings

from coupons.models import Coupon
from shop.models import Product


class Cart:
    def __init__(self, request):
        """Cart creation"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get("coupon_id")

    def __iter__(self):
        """Create an iterator for products' iteration in cart"""
        products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=products_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """Return quantity of products in a cart"""
        return sum(item["quantity"] for item in self.cart.values())

    def add_product(self, product, quantity=1, override_quantity=False):
        """Add product to cart"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
            }
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def save(self):
        """Save changes in session"""
        self.session.modified = True

    def remove_product(self, product):
        """Remove product from cart"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """Clear session and save it"""
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        """Return total price of all products in a cart"""
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())

    @property
    def coupon(self):
        """Return Coupon objects via id from cart if it exists"""
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass

    def get_discount(self):
        """Return sum of coupon discount"""
        if self.coupon:
            return self.coupon.discount / Decimal(100) * self.get_total_price()
        return Decimal(0)

    def get_total_price_with_discount(self):
        """Return total price of the cart with discount"""
        return self.get_total_price() - self.get_discount()
