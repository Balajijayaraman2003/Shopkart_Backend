from rest_framework.routers import DefaultRouter
from .views import AddressViewSet

router = DefaultRouter() 
router.register(r'address', AddressViewSet, basename='address')