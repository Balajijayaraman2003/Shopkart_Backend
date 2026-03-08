from django.urls import path
from .views import *
from .routers import router
urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name="user_registration"),
    path('login/',UserLoginView.as_view(),name="user_login"),
    path('change-password/',ChangePasswordView.as_view()),
    path('google/',GoogleLoginView.as_view(),name="user_login"),
    path('user/',UserDetailsView.as_view(),name="user_detail"),
    path('refresh/',TokenRefreshView.as_view(),name="token_refresh"),
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),

]

urlpatterns += router.urls