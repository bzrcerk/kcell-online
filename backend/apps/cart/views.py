from django.shortcuts import render
from rest_framework import viewsets

from apps.cart.models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


# Create your views here.
class CartAPIView(viewsets.ModelViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

class CartItemAPIView(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)