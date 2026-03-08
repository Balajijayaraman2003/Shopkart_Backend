from django.shortcuts import render
from rest_framework.response import Response as rs
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
import requests
from django.core.files.base import ContentFile

from .models import *
from .serializers import *
from .permissions import *
# Create your views here.
cookie_options = {
            "httponly": True,
            "secure": True,   # ⚠️ set False for local dev, True in production
            "samesite": "Lax",
            "path": "/",
            "max_age": 60 * 60 * 24,  # 1 day
        }
class UserRegistrationView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        serializer = UserCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return rs({"success":"Successfully Registered Your Account"},status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return rs(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class UserLoginView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            from rest_framework_simplejwt.tokens import RefreshToken
            user = serializer.user 
            refresh_token = RefreshToken.for_user(user)
            access_token = refresh_token.access_token
            return rs({
                "refresh_token": str(refresh_token),
                "access_token": str(access_token),
                "user":user.username,
                "email":user.email
            },status=status.HTTP_200_OK)
        else:
            return rs(serializer.errors,status=status.HTTP_401_UNAUTHORIZED)
        
class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        if serializer.is_valid():
            old_refresh_token = serializer.validated_data.get("refresh_token")
            try:
                token = RefreshToken(old_refresh_token)
                token.blacklist()
                user = Users.objects.get(id=token.payload.get("user_id"))
                username = user.username
                email = user.email
                new_refresh_token = RefreshToken.for_user(user)
                new_access_token = new_refresh_token.access_token
                return rs({
                    "refresh_token": str(new_refresh_token),
                    "access_token": str(new_access_token),
                    "user":username,
                    "email":email
                })
            except TokenError:
                return rs({"error": "Invalid or expired refresh token"}, status=400)
        return rs(serializer.errors, status=400)

        
class UserDetailsView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    

    def get_queryset(self):
        # Only allow the logged-in user to access their own address
        user = self.request.user
        return Address.objects.filter(id=user.address_id)

class GoogleLoginView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        token = request.data.get("token")
        google_resp = requests.get(
            f"https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={token}"
        )
        print(google_resp.json())
        
        if google_resp.status_code != 200:
            return rs({"error":"Invalid Google token"},status=400)
        
        data = google_resp.json()
        email = data.get("email","")
        username = data.get("given_name","")
        firstname = data.get("given_name")
        lastname = data.get("family_name","")
        profile = data.get("picture","")
        
        user,_ = Users.objects.get_or_create(
           username = username,
           defaults={"email":email,"first_name":firstname,"last_name":lastname}          
        )
        response = requests.get(profile)
        if response.status_code == 200:
            file_name = f"{user.username}_profile.jpg"
            user.profile_pic.save(file_name, ContentFile(response.content), save=True)
        
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)
        
        resp = rs({"detail":"Login Successfull",
                   "access_token":str(access_token),
                   "refresh_token":str(refresh_token)})
        resp.set_cookie("access_token", str(access_token), **cookie_options)
        resp.set_cookie("refresh_token", str(refresh_token), **cookie_options)
        return resp
        
        
import random 
from twilio.rest import Client
from django.conf import settings

otp_storage = {}

def send_otp(phone_number):
    otp = str(random.randint(100000, 999999))
    
    client = Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP is {otp}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    
    return otp,message.sid

class SendOTPView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        phone = request.data.get("phone")
        if not phone:
            return rs({"error": "Phone number required"}, status=400)
        try:
            otp,sid = send_otp(phone)
            otp_storage[phone] = otp
            
            return rs({"success":f"OTP sends to {phone}","sid":sid},status=200)
        
        except Exception as e:
            return rs({"error":e},status=400)
        
class VerifyOTPView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        print(otp_storage)
        print(request.data)
        phone = request.data.get("phone")
        otp = str(request.data.get("otp"))
        
        if not phone or not otp:
            return rs({"error": "Phone and OTP required"}, status=400)

        if otp_storage.get(phone) == otp:
            return rs({"success": "OTP verified!"}, status=200)
        return rs({"error": "Invalid OTP"}, status=400)

    
from rest_framework import status
class ChangePasswordView(APIView):
    def post(self, request):
        pwd1 = request.data.get("password")
        pwd2 = request.data.get("confirm_password")

        if not pwd1 or not pwd2:
            return rs({"error": "Password fields cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        if pwd1 != pwd2:
            return rs({"error": "Password mismatch"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = request.user  # safer than querying again
            user.set_password(pwd1)
            user.save()
            return rs({"success": "Password changed"}, status=status.HTTP_200_OK)
        except Exception as e:
            return rs({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        