from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.cart.views import CartAPIView, CartItemAPIView

router = DefaultRouter()
router.register(r'carts', CartAPIView, basename='cart')
router.register(r'cart-items', CartItemAPIView, basename='cart-item')

urlpatterns = [
    path('', include(router.urls)),
]