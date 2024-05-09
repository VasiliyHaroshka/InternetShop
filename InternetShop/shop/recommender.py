import redis

from django.conf import settings

from .models import Product

r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)


class Recommender:
    """Class for work with recommendations of products"""

    def get_product_key(self, id):
        """Create key for Redis set"""
        return f"product:{id}:bought_with"

    def product_bought(self, products: list[Product]):
        """Increase the counter of products are bought together in Redis set"""
        products_ids = [product.id for product in products]
        for product_id in products_ids:
            for with_product_id in products_ids:
                if product_id != with_product_id:
                    r.zincrby(
                        self.get_product_key(product_id),
                        1,
                        with_product_id,
                    )
