from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer


# Create your views here.
class OrderAPIView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.all()
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderDetailAPIView(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.all()
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)