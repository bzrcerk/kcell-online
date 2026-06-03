from rest_framework import serializers

from apps.products.serializers import ProductSerializer
from .models import Order, OrderItem



class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order = OrderItemSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ('id', 'user', 'full_name', 'email', 'phone_number', 'total_price')
