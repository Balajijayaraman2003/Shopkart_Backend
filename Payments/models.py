from django.db import models
from django.db.models import *
from Auth.models import Users
import uuid

# Create your models here.
class Payments(models.Model):
    payment_id = UUIDField(default=uuid.uuid4,unique=True,max_length=255)
    amount = FloatField()
    currency = CharField(max_length=10)
    stripe_intent_id = CharField(unique=True,max_length=255)
    stripe_response = JSONField()
    client_secret = CharField(max_length=255)
    payment_method = CharField(max_length=200)
    status = CharField(max_length=200)
    user = ForeignKey(Users,on_delete=CASCADE)
    order = OneToOneField("Orders.orders",on_delete=CASCADE,null=True,blank=True)
    description = TextField(max_length=255,blank=True,null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering =["created_at"]
        
    def __str__(self):
        return f"{self.payment_id}"