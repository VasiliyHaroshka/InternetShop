from django.shortcuts import render

from cart.cart import Cart
from orders.forms import OrderForm
from .models import OrderItem


def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    count=item["count"],
                )
            context = {
                "order": order,
            }
            cart.clear()
            return render(request, "orders/order/created.html", context)
    else:
        form = OrderForm()
    context = {
        "cart": cart,
        "form": form,
    }
    return render(request, "orders/order/create.html", context)
