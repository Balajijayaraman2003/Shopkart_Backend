from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description', 'category__name']  # Add fields you want to search by
    list_display = ['id','name', 'selling_price', 'category']  # Optional: for better list view
    list_filter = ['category']  # Optional: adds sidebar filters

class CategoriesAdmin(admin.ModelAdmin):
    search_fields =["name"]
    list_display = ["name"]
    list_filter =["created_at"]
admin.site.register(Categories,CategoriesAdmin)
# admin.site.register(Product)
admin.site.register(ProductImages)
admin.site.register(Tags)

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display =["name","start_date","end_date","is_active"]

admin.site.register(Size)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(WhishList)