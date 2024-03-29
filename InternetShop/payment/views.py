from decimal import Decimal

import stripe

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from myshop.settings import STRIPE_SECRET_KEY, STRIPE_API_VERSION
from orders.models import Order

stripe.api_key = STRIPE_SECRET_KEY
stripe.api_version = STRIPE_API_VERSION


def payment_process(request):
    """Create session of payment, checkout session and redirect to stripe payment form"""
    order_id = request.session.get("order_id", None)
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        success_url = request.build_absolute_uri(reverse("payment:completed"))
        cancel_url = request.build_absolute_uri(reverse("payment:cancel"))

        session_data = {
            "mode": "payment",
            "client_reference_id": order_id,
            "success_url": success_url,
            "cancel_url": cancel_url,
            "line_items": [],
        }

        for item in order.items.all():
            session_data["line_items"].append({
                "price_data": {
                    "unit_amount": int(item.price * Decimal("100")),
                    "currency": "usd",
                    "product_data": {"name": item.product.name},
                    "count": item.count,
                }
            })

        session = stripe.checkout.Session.create(**session_data)
        return redirect(session.url, code=303)

    else:
        return render(request, "payment/process.html", locals())


def payment_completed(request):
    return render(request, "payment:completed.html")


def payment_canceled(request):
    return render(request, "payment:canceled.html")
