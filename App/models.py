from django.db import models
from django.db.models import *
import uuid
from Auth.models import Users
# Create your models here.

class Categories(models.Model):
    code = UUIDField(max_length=255,default=uuid.uuid4,unique=True,editable=False)
    name = CharField(max_length=255)
    image = ImageField(upload_to="Cetegory_Images")
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        
class ProductImages(models.Model):
    image = ImageField(upload_to="Product_Images")
    created_at = DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
    def __str__(self):
        return f"{self.image}"

class Tags(models.Model):
    name = CharField(max_length=200)
    variant = CharField(max_length=200,default="danger")
    created_at = DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
    def __str__(self):
        return f"{self.name}"
    
class Size(models.Model):
    name = CharField(max_length=200)
    desc = CharField(max_length=200,null=True,blank=True)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    code = UUIDField(max_length=255,default=uuid.uuid4,unique=True)
    name = CharField(max_length=255)
    category = ForeignKey(Categories,on_delete=CASCADE,null=True,blank=True)
    image = ForeignKey(ProductImages,on_delete=SET_NULL,null=True,blank=True)
    description = TextField(max_length=2500)
    short_description = TextField(max_length=500)
    brand = CharField(max_length=255)
    old_price = FloatField()
    selling_price = FloatField()
    spec = JSONField(null=True,blank=True)
    rating = DecimalField(max_digits=3, decimal_places=1)
    rating_count = IntegerField()
    sizes = ManyToManyField(Size,null=True,blank=True)
    tags = ManyToManyField(Tags,blank=True)
    slug = SlugField(unique=False)
    in_stock = BooleanField(default=True)
    stock_quantity = IntegerField()
    discount_percent = FloatField()
    created_at = DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        
    def __str__(self):
        return f"{self.name} {self.category} {self.slug}"
    
    
    
class Offer(models.Model):
    name = CharField(max_length=255)  # e.g. "Christmas Sale"
    description = TextField(blank=True, null=True)
    start_date = DateTimeField()
    end_date = DateTimeField()
    products = ManyToManyField("Product", related_name="offers", blank=True)

    class Meta:
        verbose_name = "Offer"
        verbose_name_plural = "Offers"

    def is_active(self):
        from django.utils import timezone
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def __str__(self):
        return self.name
    
class Review(models.Model):
    user = ForeignKey(Users,on_delete=CASCADE)
    product = ForeignKey(Product,on_delete=CASCADE,related_name="reviews")
    rating = DecimalField(max_digits=3, decimal_places=1)
    review = TextField(max_length=500)
    image = ImageField(upload_to="review_images",null=True,blank=True)
    date = DateField(auto_now_add=True,null=True,blank=True)
    time = TimeField(auto_now_add=True,null=True,blank=True)
    created_at = DateTimeField(auto_now_add=True,null=True,blank=True)
    
class Cart(models.Model):
    user = ForeignKey(Users,on_delete=CASCADE)
    product = ForeignKey(Product,on_delete=CASCADE,related_name="products")
    quantity = IntegerField(default=1)
    created_at = DateTimeField(auto_now_add=True)
    
class WhishList(models.Model):
    user = ForeignKey(Users,on_delete=CASCADE)
    product = ForeignKey(Product,on_delete=CASCADE,related_name="product")
    created_at = DateTimeField(auto_now_add=True)