from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import AddProductToCartForm
from coupons.forms import CouponApplyForm
from shop.models import Product


@require_POST
def add_product_to_cart(request, product_id):
    """Add product to cart or change its quantity if product is already in a cart"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = AddProductToCartForm(request.POST)

    if form.is_valid():
        data = form.cleaned_data
        cart.add_product(
            product=product,
            quantity=data["quantity"],
            override_quantity=data["override"],
        )

    return redirect("cart:cart_detail")


@require_POST
def remove_product_from_cart(request, product_id):
    """Remove product from a cart"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove_product(product)
    return redirect("cart:cart_detail")


def cart_detail(request):
    """Show products in a cart"""
    cart = Cart(request)
    for item in cart:
        item["update_quantity_form"] = AddProductToCartForm(
            initial={
                "quantity": item["quantity"],
                "override": True,
            }
        )
    coupon_apply_form = CouponApplyForm()
    context = {
        "cart": cart,
        "coupon_apply_form": coupon_apply_form,
    }
    return render(request, "cart/detail.html", context=context)
