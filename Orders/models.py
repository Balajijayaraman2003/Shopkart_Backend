from django.db import models
import uuid
from Auth.models import Address, Users
from App.models import Product
from Payments.models import Payments

class ShippingAddress(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="shipping_addresses")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="shipping_addresses")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Shipping to: {self.address}"


class Orders(models.Model):
    order_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    address = models.OneToOneField(ShippingAddress, on_delete=models.CASCADE,related_name="shipping_addresses")
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Order Placed", "Order Placed"),
        ("Ready For Shipping", "Ready For Shipping"),
        ("Shipped", "Shipped"),
        ("Out For Delivery", "Out For Delivery"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default="Pending")
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    payment_method = models.CharField(max_length=255, default="cash-on-delivery")
    payment_status = models.CharField(max_length=255,default="Pending")
    payment_details = models.OneToOneField(Payments,on_delete=models.CASCADE,null=True,blank=True,related_name="order_payment_details")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order No: {self.id} {self.order_id}"

class OrderProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="order_products")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Ordered Product"
        verbose_name_plural = "Ordered Products"
        
    def product_code(self):
        return self.product.code
    
#implement refound for the product cancellation