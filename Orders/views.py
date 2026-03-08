from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from Auth.permissions import IsOwner
from .models import Orders
from .serializers import OrdersSerializer
from Payments.models import Payments
from rest_framework.pagination import CursorPagination
from django.shortcuts import get_object_or_404


class CurserPaginationClass(CursorPagination):
    page_size = 30
    ordering = "-created_at"
    
class OrdersViewSet(viewsets.ModelViewSet):
    pagination_class= CurserPaginationClass
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticated]
        
    def get_queryset(self):
        print(self.request.data)
        return Orders.objects.filter(user=self.request.user).exclude(status="Pending")

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class GetOrderDetails(APIView):
    permission_classes = [AllowAny]  # safer than AllowAny

    def get(self, request, order_id=None):
        if not order_id:
            return Response({"error": "Missing Order id"}, status=400)

        order = get_object_or_404(Orders, order_id=order_id, user=request.user)
        serializer = OrdersSerializer(order)
        return Response(serializer.data, status=200)
