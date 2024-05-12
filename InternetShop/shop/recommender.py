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

    @staticmethod
    def get_product_key(id):
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

    def suggest_products(self, products: list[Product], max_count=6):
        """Get products are bought together for recommendations"""
        product_ids = [product.id for product in products]

        if len(product_ids) == 1:
            suggestions = r.zrange(
                self.get_product_key(product_ids[0]),
                0,
                -1,
                desc=True,
            )[:max_count]

        else:
            str_ids = "".join([str(id) for id in product_ids])
            tmp_key = f"tmp_{str_ids}"  # временный ключ

            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)

            r.zrem(tmp_key, *product_ids)  # del the same

            suggestions = r.zrange(
                tmp_key,
                0,
                -1,
                desc=True,
            )[:max_count]

            r.delete(tmp_key)

        suggestion_products_ids = [int(id) for id in suggestions]
        suggestion_products = list[Product.objects.filter(id__in=suggestion_products_ids)]
        suggestion_products.sort(key=lambda x: suggestion_products_ids.index(x.id))

        return suggestion_products

    def clear_recommendations(self):
        """Clear recommendations from Redis"""
        for id in Product.objects.values_list("id", flat=True):
            r.delete(self.get_product_key(id))
