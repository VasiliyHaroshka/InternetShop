from io import BytesIO

import weasyprint
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from myshop.settings import MAIL_RU_POST
from orders.models import Order


@shared_task
def payment_complete(order_id):
    """Task for sending an email after the order was paid successful"""
    order = get_object_or_404(Order, id=order_id)
    subject = f"Internet Shop - Invoice number {order_id}"
    message = "The invoice is attached to your mail."
    email = EmailMessage(
        subject,
        message,
        MAIL_RU_POST,
        [order.email],
    )
    context = {
        "order": order,
    }
    html = render_to_string("orders/order/pdf.html", context)
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT/"css/pdf.html")]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    email.attach(
        f"order_{order_id}.pdf",
        out.getvalue(),
        "application/pdf",
    )
    email.send()
