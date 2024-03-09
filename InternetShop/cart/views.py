from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import AddProductToCart
from shop.models import Product


@require_POST
def add_product_to_cart(request, product_id):
    """Add product to cart or change its count if product is already in a cart"""
    cart = Cart()
    product = get_object_or_404(Product, id=product_id)
    form = AddProductToCart(request.POST)

    if form.is_valid():
        data = form.cleaned_data
        cart.add_product(
            product=product,
            count=data["count"],
            override_count=data["override"],
        )

    return redirect("cart:cart_detail")


@require_POST
def remove_product_from_cart(request, product_id):
    """Remove product from a cart"""
    cart = Cart()
    product = get_object_or_404(Product, id=product_id)
    cart.remove_product(product)
    return redirect("cart:cart_detail")


def cart_detail(request):
    """Show products in a cart"""
    cart = Cart(request)
    context = {
        "cart": cart,
    }
    return render(request, "cart/detail.html", context=context)
