from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    spending_limit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class Item(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bought = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} x {self.name} (User: {self.shopping_list.user.username})"

    @property
    def total_cost(self):
        return self.quantity * self.price

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField(default=timezone.now().date() + timedelta(days=7))

    def __str__(self):
        return self.name
