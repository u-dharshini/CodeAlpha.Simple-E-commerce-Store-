from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.URLField(blank=True)  # Product image URL

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = (
        ('cart', 'Cart'),
        ('placed', 'Placed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='cart')

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.status})"

    def total_price(self):
        return self.product.price * self.quantity
