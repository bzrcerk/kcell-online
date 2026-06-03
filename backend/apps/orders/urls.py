from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrderAPIView, OrderDetailAPIView

router = DefaultRouter()
router.register(r'orders', OrderAPIView, basename='orders')
router.register(r'order-items', OrderDetailAPIView, basename='order-items')

urlpatterns = [
    path('', include(router.urls)),
]