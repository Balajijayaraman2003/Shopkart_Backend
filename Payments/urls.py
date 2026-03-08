from django.urls import path

from . views import *

urlpatterns = [
    path("pay/",StripePaymentCreationView.as_view(),name="payment_via_stripe"),
    path('stripe/webhook/',StripeWebhookView.as_view(),name="stripe-webhook")
]