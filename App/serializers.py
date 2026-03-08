from rest_framework import serializers
from .models import *

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields =["image"]
        depth = 1
        
class ProductSerializer(serializers.ModelSerializer):
    image = ProductImageSerializer(read_only=True)
    class Meta:
        model = Product
        fields =["id","name","category","image","description","short_description","old_price","selling_price",
                 "rating","rating_count","tags","slug","in_stock","stock_quantity","discount_percent","brand","spec","code"]
        depth=1
class CategorySerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Review
        fields = ["id", "product","user", "rating", "review", "image", "date", "time"]
        read_only_fields =["user"]

    def validate(self, data):
        print(data)  # Now this will include 'product'
        return data


class CartSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True   # accept product ID when creating/updating
    )
    product_details = ProductSerializer(source="product", read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "product", "product_details", "quantity", "created_at"]
        read_only_fields = ["user", "created_at"]

        
class WhishListSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True   # accept product ID when creating/updating
    )
    product_details = ProductSerializer(source="product", read_only=True)
    class Meta:
        model = WhishList
        fields = ["id","user","product","product_details","created_at"]
        read_only_fields=["user"]
        depth=1