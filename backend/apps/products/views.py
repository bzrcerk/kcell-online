from django.shortcuts import render
from rest_framework import viewsets

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


def catalog_page(request):
    products = Product.objects.select_related('category').all()
    return render(request, 'templates/catalog.html', {'products': products})

# Create your views here.
class CategoryAPIView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductAPIView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer