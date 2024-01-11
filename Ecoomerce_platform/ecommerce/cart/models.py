# pylint: disable=no-member
"""models"""
from django.db import models
from users.models import User
from product.models import Product

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('CartItem', related_name='cart_items')

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def calculate_total_cost(self):
        return (self.product.price * self.quantity)