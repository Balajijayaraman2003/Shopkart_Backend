from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Orders, OrderProducts, ShippingAddress
from Payments.models import Payments

class OrderProductsInline(admin.StackedInline):
    model = OrderProducts
    extra = 0
    readonly_fields = ["product_code","product_category","product_amount"]

    def product_code(self, obj):
        if obj.product:
            return f'{obj.product.code} '
        return "-"
    def product_category(self,obj):
        if obj.product:
            return f'{obj.product.category}'
    def product_amount(self,obj):
        if obj.product:
            return f'{obj.product.selling_price}'
class PaymentInline(admin.StackedInline):
    model = Payments
    verbose_name = "Payment Detail"
    extra = 0
    exclude = ["stripe_response","description"]
    
    
@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ["order_id", "address_table","created_at","payment_details"]
    search_fields = ["order_id", "user__email","id"]
    list_filter = ["status", "created_at", "payment_method"]
    list_display = ["order_id", "id", "user", "amount", "payment_method", "status", "created_at","payment_details"]
    inlines = [OrderProductsInline,PaymentInline]

    fieldsets = (
        ("Order Info", {
            "fields": ("order_id", "user", "status", "amount", "payment_method","created_at","payment_details","payment_status" )
        }),
        ("Shipping Address", {
            "fields": ("address_table",)
        }),
    )
        



    def address_table(self, obj):
        if obj.address and obj.address.address:
            addr = obj.address.address
            html = f"""
            <table style='border-collapse: collapse; width: 100%;'>
                <tr><th style='text-align:left;'>Full Name</th><td>{addr.full_name}</td></tr>
                <tr><th style='text-align:left;'>Mobile</th><td>{addr.mobile}</td></tr>
                <tr><th style='text-align:left;'>House No.</th><td>{addr.house_no}</td></tr>
                <tr><th style='text-align:left;'>Area</th><td>{addr.area}</td></tr>
                <tr><th style='text-align:left;'>Landmark</th><td>{addr.landmark}</td></tr>
                <tr><th style='text-align:left;'>City</th><td>{addr.city}</td></tr>
                <tr><th style='text-align:left;'>Pincode</th><td>{addr.pincode}</td></tr>
                <tr><th style='text-align:left;'>State</th><td>{addr.state}</td></tr>
                <tr><th style='text-align:left;'>Country</th><td>{addr.country}</td></tr>
            </table>
            """
            return mark_safe(html)
        return "No address available"

    address_table.short_description = "Shipping Address"

# Register other models
admin.site.register(ShippingAddress)
admin.site.register(OrderProducts)