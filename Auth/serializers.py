from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user_id','first_name','last_name','username','email','phno','profile_pic',"is_active","address"]
        depth=1
class UserCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    cpassword = serializers.CharField(write_only=True)
    class Meta:
        model = Users
        fields = ['first_name','last_name','username','email','phno','profile_pic','password','cpassword','address']
        read_only_fields =["last_login","is_superuser","is_staff","is_active"]
    
    def validate(self, data):
        print(data)
        pwd = data.get("password")
        cpwd = data.get("cpassword")
        if not pwd==cpwd:
            raise serializers.ValidationError({"error":"Password miss match"})
        return data
    
    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("cpassword")
        
        user = Users.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get("username")
        password= data.get("password")
        user = authenticate(username=username,password=password)
        if user is None:
            raise(serializers.ValidationError({"error":"No User with this username or password"}))
        if user and not user.is_active:
            raise(serializers.ValidationError({"error":"This account is in active. please contact our support..."}))
        self.user = user
        return data
    
class TokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(write_only=True)
    
    def validate(self, data):
        refresh_token = data.get("refresh_token")
        try:
            token = RefreshToken(refresh_token)
            print("Token Verified")
            return data
        except Exception as e:
            raise serializers.ValidationError({"token error":e})
        
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        user = self.context.get("request").user
        if not isinstance(user, Users):
            raise serializers.ValidationError("Invalid user")

        # Create address and link to user
        address = Address.objects.create(user=user, **validated_data)
        user.address = address
        user.save()
        return address

    def update(self, instance, validated_data):
        user = self.context.get("request").user
        if not isinstance(user, Users):
            raise serializers.ValidationError("Invalid user")

        # Ensure the logged-in user's address is this instance
        if user.address != instance:
            raise serializers.ValidationError("You can only update your own address")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
