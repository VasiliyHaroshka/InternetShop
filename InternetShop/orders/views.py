from django.shortcuts import render, redirect
from django.urls import reverse

from cart.cart import Cart
from orders.forms import OrderForm
from .models import OrderItem
from .tasks import order_created


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
            order_created.delay(order.id)
            request.session["order_id"] = order.id
            return redirect(reverse("payment:process"))
    else:
        form = OrderForm()
    context = {
        "cart": cart,
        "form": form,
    }
    return render(request, "orders/order/create.html", context)
