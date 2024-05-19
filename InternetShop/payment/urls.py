from django.utils.translation import gettext_lazy as _
from django.urls import path

from .views import payment_process, payment_completed, payment_canceled
from .webhooks import stripe_webhook

app_name = "payment"

urlpatterns = [
    path(_("process/"), payment_process, name="process"),
    path(_("completed/"), payment_completed, name="completed"),
    path(_("canceled/"), payment_canceled, name="canceled"),
    path("webhook/", stripe_webhook, name="stripe-webhook"),
]
