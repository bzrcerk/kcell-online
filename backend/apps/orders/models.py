from django.contrib.auth.models import User
from django.db import models

from apps.products.models import Product


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=250)
    email = models.EmailField()
    phone_number = models.IntegerField()
    address = models.CharField(max_length=250)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)