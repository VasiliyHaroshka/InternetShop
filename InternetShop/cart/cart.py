from decimal import Decimal

from django.conf import settings

from shop.models import Product


class Cart:
    def __init__(self, request):
        """Cart creation"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add_product(self, product, count=1, override_count=False):
        """Add product to cart"""
        product_id = product.id
        if product_id not in self.cart:
            self.cart[product_id] = {
                "count": 0,
                "price": str(product_id.price),
            }
        if override_count:
            self.cart[product_id]["count"] = count
        else:
            self.cart[product_id]["count"] += count
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

    def __iter__(self):
        """Create an iterator for products' iteration in cart"""
        products_id = self.cart.keys()
        products = Product.objects.filter(id__in=products_id)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["count"]
            yield item

    def __len__(self):
        """Return len of cart"""
        return sum(item["count"] for item in self.cart.values())

    def get_total_price(self):
        """Return total price of all products in a cart"""
        return sum(Decimal(item["price"] * item["count"]) for item in self.cart.values())

    def clear(self):
        """Clear session and save it"""
        del self.session[settings.CART_SESSION_ID]
        self.save()
