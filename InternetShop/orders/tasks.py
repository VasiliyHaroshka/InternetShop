from celery import shared_task
from django.core.mail import send_mail

from orders.models import Order


@shared_task
def order_created(order_id):
    """Send email message when order create successfully"""
    order = Order.objects.get(id=order_id)
    subject = f"Order № {order.id}"
    message = (f"Hi, {order.first_name}.\nYour order was created successfully. "
               f"Number of your order is {order.id}")
    mail_sent = send_mail(subject, message, "mysite@gmail.com", [order.email])
    return mail_sent
