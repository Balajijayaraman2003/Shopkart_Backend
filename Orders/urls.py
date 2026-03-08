from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path
router = DefaultRouter()
router.register(r'orders', OrdersViewSet, basename='orders')
urlpatterns =[
    path('order-details/<str:order_id>/',GetOrderDetails.as_view())
]
urlpatterns += router.urls