from django.contrib import admin
from .models import *
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken,OutstandingToken
from django.utils.safestring import mark_safe

class UseresManager(admin.ModelAdmin):
    readonly_fields = ["address_table","address"]
    def address_table(self, obj):
        if obj.address:
            html = f"""
            <table style='border-collapse: collapse; width: 100%;'>
                <tr><th style='text-align:left;'>Full Name</th><td>{obj.address.full_name}</td></tr>
                <tr><th style='text-align:left;'>Mobile</th><td>{obj.address.mobile}</td></tr>
                <tr><th style='text-align:left;'>House No.</th><td>{obj.address.house_no}</td></tr>
                <tr><th style='text-align:left;'>Area</th><td>{obj.address.area}</td></tr>
                <tr><th style='text-align:left;'>Land Mark</th><td>{obj.address.landmark}</td></tr>
                <tr><th style='text-align:left;'>City</th><td>{obj.address.city}</td></tr>
                <tr><th style='text-align:left;'>Pincode</th><td>{obj.address.pincode}</td></tr>
                <tr><th style='text-align:left;'>State</th><td>{obj.address.state}</td></tr>
                <tr><th style='text-align:left;'>Contry</th><td>{obj.address.country}</td></tr>
            </table>
            """
            return mark_safe(html)
        return "No address available"
    address_table.short_description = ""
    
    fieldsets = (
        ("Personal Info", {
            'fields': ['user_id','first_name', 'last_name', 'username', 'email', 'phno',"address","stripe_customer_id","profile_pic"]
        }),
        ("Login Info", {
            'fields': ['password', 'last_login', 'date_joined']
        }),
        ("Account Status", {
            'fields': ['is_active', 'is_staff', 'is_superuser']
        }),
        ("Permissions", {
            'fields': ['groups', 'user_permissions']
        }),
        ("Address Info", {
            'fields': ['address_table']
        }),
    )


class AddressManger(admin.ModelAdmin):
    search_fields=["city","pincode","area"]
    list_filter =["city","state","country"]
admin.site.register(Users,UseresManager)
admin.site.register(Address,AddressManger)
