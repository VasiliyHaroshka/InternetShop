from .cart import Cart


def cart(request):
    """Context processor add cart to context"""
    return {"cart": Cart(request)}
