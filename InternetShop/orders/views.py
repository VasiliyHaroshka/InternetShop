from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
import weasyprint

from cart.cart import Cart
from orders.forms import OrderForm
from .models import OrderItem, Order
from .tasks import order_created


def order_create(request):
    """Create an order and applying a discount if it is"""
    cart = Cart(request)
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )

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


@staff_member_required
def admin_order_detail(request, order_id):
    """Show the information about the order"""
    order = get_object_or_404(Order, id=order_id)
    context = {
        "order": order,
    }
    return render(request, "admin/orders/order/detail.html", context)


@staff_member_required
def admin_order_pdf(request, order_id):
    """Generate report about the order in .pdf"""
    order = get_object_or_404(Order, id=order_id)
    context = {
        "order": order,
    }
    html = render_to_string("orders/order/pdf.html", context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"filename=order_{order_id}.pdf"

    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[
            weasyprint.CSS(settings.STATIC_ROOT/"css/pdf.css")
        ]
    )
    return response
