from rest_framework import serializers
from .models import *

from rest_framework import serializers

class StripeSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    currency = serializers.CharField()
    
class PaymentSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields =["payment_id","stripe_intent_id","amount","currency",
                 "stripe_response","payment_method","status","user",
                 "description","order"]