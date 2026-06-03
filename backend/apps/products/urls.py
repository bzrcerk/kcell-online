from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProductAPIView, CategoryAPIView, catalog_page

router = DefaultRouter()
router.register(r'products', ProductAPIView, basename='products')
router.register(r'categories', CategoryAPIView, basename='categories')


urlpatterns = [
    path('', include(router.urls)),
    path('', catalog_page, name='catalog_page')
]