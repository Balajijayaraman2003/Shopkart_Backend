from django.contrib import admin
from .models import *
# Register your models here.
class OrderInline(admin.StackedInline):
    from Orders.models import Orders
    model = Orders
    extra = 0
    readonly_fields =["order_id","amount","address","status","user","payment_method","payment_status"]
    
@admin.register(Payments)
class PaymentAdmin(admin.ModelAdmin):
    readonly_fields=["stripe_intent_id","payment_id","updated_at","created_at"]
    list_display=["payment_id","id","amount","currency","date"]
    ordering = ["-created_at"]
    inlines=[OrderInline]
    fieldsets = (
    ("Payment Details", {
        "fields": ["payment_id", "amount", "currency","stripe_intent_id","stripe_response","client_secret","payment_method","status","user","order","description" ,"updated_at","created_at"]
    }),
)

    def date(self, obj):
        return obj.created_at.date()    
    date.short_description = "Date"