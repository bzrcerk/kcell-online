from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    def __str__(self):
        return self.title
