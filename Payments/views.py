from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response as rs
from rest_framework.permissions import AllowAny
from django.conf import settings
import stripe
from .models import *
from .seializers import *
from Orders.models import Orders,OrderProducts
# Create your views here.
# payment = Payments.objects.get(order__order_id="0a905d6a-4d0b-4633-b852-5957eddb1bf9")
# print(payment.payment_method)

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripePaymentCreationView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        serializer = StripeSerializer(data=request.data)
        if serializer.is_valid():
            
            intent = stripe.PaymentIntent.create(
                amount= request.data.get("amount"),
                currency= request.data.get("currency"),                               
                automatic_payment_methods={"enabled":True},
                # payment_method_types=["card"],
                metadata={
                    "order_id":str(request.data.get("order_id")),
                    "user_id": str(request.data.get("user_id")),
                }
            )
            print("Payment Intent")
            return rs(
                {
                    "clientSecret":intent.client_secret
                }
            )
        return rs({
            "error":serializer.errors
        })

from rest_framework.views import APIView
from rest_framework.response import Response as rs
from rest_framework.permissions import AllowAny
from django.conf import settings
import stripe
from .models import Payments
from Orders.models import Orders

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print("Webhook Called")
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
            
        except ValueError:
            return rs({"error": "Invalid payload"}, status=400)
        except stripe.error.SignatureVerificationError:
            return rs({"error": "Invalid signature"}, status=400)
        except Exception as e:
            return rs({"error": str(e)}, status=400)

        payment_intent = event['data']['object']

        metadata = payment_intent.get('metadata', {})
        user_id = metadata.get("user_id")
        order_id = metadata.get("order_id")
        print(user_id,order_id)
        
        try:
            user = Users.objects.get(user_id=user_id)
            user_id = user.id
            print("User id:",user_id)
            print("Order id:",order_id)
            order_id = Orders.objects.get(order_id=order_id)
            order_id = order_id.id
        except Exception as e:
            print(e)
    
        print(event['type'])       
        if event['type'] == "payment_intent.succeeded":
            payment_method_id = payment_intent['payment_method']
            payment_method_obj = stripe.PaymentMethod.retrieve(payment_method_id)
            method_type = payment_method_obj['type']
            try:
            
                payment_data = {
                    "stripe_intent_id": payment_intent['id'],
                    "amount": payment_intent['amount']/100,
                    "currency": payment_intent['currency'],
                    "payment_method": method_type,
                    "status": payment_intent['status'],
                    "client_secret": payment_intent["client_secret"],
                    "user_id": user_id,
                    "order_id": order_id,
                    "stripe_response": payment_intent
                }

                payment = Payments.objects.create(**payment_data)

                order = Orders.objects.get(id=order_id)
                print(order)
                order.payment_details = payment
                order.status= "Order Placed"
                order.payment_status=payment_intent['status']
                order.payment_method = method_type
                order.save()
                print("payment details added")
                ordered_products = OrderProducts.objects.get(order=order_id)
                print(ordered_products)
                invoice = stripe.Invoice.create(
                    customer=user.stripe_customer_id,
                    collection_method='send_invoice',
                    days_until_due=7,
                    metadata={
                    "order_id": metadata.get("order_id"),
                    "user_id": metadata.get("user_id")
                    })
                stripe.InvoiceItem.create(
                    customer=user.stripe_customer_id,
                    amount = payment_intent['amount'],
                    currency=payment_intent['currency'],
                    invoice= invoice.id
                )
                print(payment_intent['amount'])
                finalized_invoice = stripe.Invoice.finalize_invoice(invoice.id)
                stripe.Invoice.send_invoice(finalized_invoice.id)
            except Orders.DoesNotExist:
                    print(f"⚠️ Order {order_id} not found")
            except Exception as e:
                print(e)
        else:    
            order = Orders.objects.filter(id=order_id)
            order.update(status="Pending")
        if event['type'] in ['payment_intent.payment_failed', 'payment_intent.canceled']:
            print(f"❌ Payment failed or canceled: {payment_intent['id']}")
            Orders.objects.filter(id=order_id).delete()
            print("Order Deleted: ",order_id)
        print(event['type'])
        return rs({"status": "Webhook received"}, status=200)