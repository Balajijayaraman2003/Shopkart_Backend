from django.db import models
from django.db.models import *
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

class Address(models.Model):
    full_name = CharField(max_length=200)
    mobile = CharField(max_length=20)
    country = CharField(max_length=200)
    house_no = CharField(max_length=200)
    area = CharField(max_length=200)
    landmark = CharField(max_length=200)
    pincode = CharField(max_length=10)
    city = CharField(max_length=200)
    state = CharField(max_length=200)
    
    def __str__(self):
        return f"Mobile: {self.mobile} Pincode {self.pincode} city: {self.city}"
    
    class Meta:
        verbose_name_plural ="Address"
        verbose_name="Address"
        
class Users(AbstractUser):
    user_id = UUIDField(max_length=255,default=uuid.uuid4,unique=True)
    phno = CharField(max_length=20)
    address = ForeignKey(Address,on_delete=SET_NULL,null=True,blank=True)
    profile_pic = ImageField(upload_to="profiles",null=True,blank=True)
    stripe_customer_id = CharField(max_length=255,null=True,blank=True)