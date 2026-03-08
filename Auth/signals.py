from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.conf import settings
import stripe

from .models import Users

stripe.api_key = settings.STRIPE_SECRET_KEY

@receiver(post_save,sender=Users)
def create_stripe_cutomer_id(sender,instance,created,*args,**kwargs):
    if created and not instance.stripe_customer_id:
        try:
            customer = stripe.Customer.create(
            email=instance.email,
            metadata={"user_id":str(instance.user_id)}
            )
            instance.stripe_customer_id = customer.id
            instance.save()
        except Exception as e:
            print("stripe customer creation failed: ",e)
            

@receiver(pre_save, sender=Users)
def hash_password(sender, instance, *args, **kwargs):
    # Only hash if the password is not already hashed
    raw_password = instance.password
    if not raw_password.startswith('pbkdf2_'):  # Django hashes start like this
        instance.set_password(raw_password)
        print("Password Hashed")

        


