from rest_framework import serializers
from .models import ShippingAddress, Orders, OrderProducts
from App.models import Product
from Auth.models import Address
from Payments.models import Payments
from App.serializers import ProductSerializer
class ShippingAddressSerializer(serializers.ModelSerializer):
    address_details = serializers.DictField(write_only=True, required=False)
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), required=False)

    class Meta:
        model = ShippingAddress
        fields = ["id", "user", "address", "created_at", "address_details"]
        read_only_fields = ["user", "created_at"]
    
    def create(self, validated_data):
        address_data = validated_data.pop("address_details", None)
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required to create a shipping address.")

        if address_data:
            address = Address.objects.create(**address_data)
        else:
            if not hasattr(request.user, "address"):
                raise serializers.ValidationError("You don't have a default address.")
            address = request.user.address

        return ShippingAddress.objects.create(address=address, user=request.user)

class OrderProductsSerializer(serializers.ModelSerializer):
    # Used during creation (write-only)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    # Used during retrieval (read-only)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderProducts
        fields = ["product_id", "product", "quantity"]

    

class OrdersSerializer(serializers.ModelSerializer):
    products = OrderProductsSerializer(many=True, source="order_products")
    address = ShippingAddressSerializer(required=False)

    class Meta:
        model = Orders
        fields = ["order_id", "address", "status", "user", "products", "payment_method", "amount","payment_details"]
        read_only_fields = ["order_id", "amount", "user", "address",]
        depth = 1
    def create(self, validated_data):
        products_data = validated_data.pop("order_products")
        address_data = validated_data.pop("address", None)

        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required to place an order.")

        # Create or reuse shipping address
        if address_data:
            shipping_address_serializer = ShippingAddressSerializer(data=address_data, context=self.context)
            shipping_address_serializer.is_valid(raise_exception=True)
            address = shipping_address_serializer.save()
        else:
            if not hasattr(request.user, "address") or not request.user.address:
                raise serializers.ValidationError({"error":"A shipping address is required. Please add one to proceed with your order."})
            address = ShippingAddress.objects.create(user=request.user, address=request.user.address)

            

        # Calculate total amount
        total_amount = sum([
            item["product"].selling_price * item["quantity"]
            for item in products_data
        ])

        # Create order
        order = Orders.objects.create(
            address=address,
            amount=total_amount,
            user=request.user,
            **validated_data
        )
        order.status = "Order Placed" if validated_data.get("payment_method") == "cash-on-delivery" else "Pending"
        order.save()

        # Create order items
        for product_data in products_data:
            OrderProducts.objects.create(order=order, **product_data)

        return order