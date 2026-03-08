from django.shortcuts import render
from rest_framework.response import Response as rs
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView,RetrieveAPIView,CreateAPIView,ListCreateAPIView,DestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.pagination import CursorPagination
from django.db.models import Q

from .models import *
from .serializers import *
# Create your views here.

class CurserPaginationSetup(CursorPagination):
    page_size = 30
    page_size_query_param = 'limit'   # ?limit=50
    max_page_size = 100
    ordering = ["selling_price"]


class WordSearchFilter(SearchFilter):
    def get_search_terms(self, request):
        # Split query into individual words
        params = request.query_params.get(self.search_param, '')
        return params.replace(',', ' ').split()

class ProductView(ListAPIView):
    permission_classes=[AllowAny]
    queryset = Product.objects.all()
    pagination_class = CurserPaginationSetup
    pagination_class.ordering=["name"]
    pagination_class.page_size=30
    serializer_class = ProductSerializer
    
class SearchProductView(ListAPIView):
    permission_classes=[AllowAny]
    queryset = Product.objects.all()
    pagination_class = CurserPaginationSetup
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,WordSearchFilter,OrderingFilter]
    filterset_fields = ['category','brand','selling_price']
    search_fields = ["name","description","brand"]
    ordering_fields = ["name","selling_price"]

class ProductDetailedView(RetrieveAPIView):
    permission_classes = [AllowAny]
    pagination_class = CurserPaginationSetup
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "code"


class RetriveSimilarProductsView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes =[AllowAny]
    pagination_class = CurserPaginationSetup
    def get_queryset(self):
        print(self.request.user)
        product_code = self.kwargs.get("code")
        print(product_code)
        try:
            product = Product.objects.get(code=product_code)
            category = product.category
            brand = product.brand
            queryset = Product.objects.filter(
                Q(category=category) | Q(brand=brand)
            ).exclude(code=product_code)
            queryset = queryset.order_by(
                'brand'
            )
            return queryset
        except Product.DoesNotExist:
            return Product.objects.none()

class CategoriesView(ListAPIView):
    pagination_class = CurserPaginationSetup
    permission_classes=[AllowAny]
    queryset = Categories.objects.all()
    serializer_class = CategorySerilaizer
    
class ProductBasedOnCategoriesView(ListAPIView):
    pagination_class = CurserPaginationSetup
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        category_code = self.kwargs.get("id")
        return Product.objects.filter(
            category__code= category_code
        )
    
class ReviewsView(ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes =[AllowAny]
    
    def get_queryset(self):
        product_code = self.kwargs.get("code")
        print(product_code)
        return Review.objects.filter(product__code=product_code)
    
class ReviewsCreateView(CreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class TopDealsView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = CurserPaginationSetup
    
    def get_queryset(self):
        return Product.objects.filter(
            Q(tags__name__in=["Top Deals","Trending"]) | Q(discount_percent__gt=20)
        ).distinct()

class NewArrivalsView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = CurserPaginationSetup
    
    def get_queryset(self):
        return Product.objects.filter(tags__name__in=["New Arrival"])
    
class CartView(ModelViewSet):
    serializer_class = CartSerializer
    def get_queryset(self):
        user =  self.request.user
        return Cart.objects.filter(user = user)
    
    def perform_create(self, serializer):
        print(self.request.data)
        return serializer.save(user=self.request.user)

class WhishListView(ListCreateAPIView,DestroyAPIView):
    serializer_class = WhishListSerializer
    
    def get_queryset(self):
        user = self.request.user
        return WhishList.objects.filter(user = user)
    
    def perform_create(self, serializer):
        return serializer.save(user = self.request.user)
    
class WishListDestroyView(DestroyAPIView):
    serializer_class = WhishListSerializer
    queryset = WhishList.objects.all()


