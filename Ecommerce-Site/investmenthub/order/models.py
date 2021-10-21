from django.db import models

from product.models import Product
from client.models import Client

# Create your models here.
class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=False) # Change to true when making real orders
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2)
    client = models.ManyToManyField(Client, related_name='orders')

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.last_name + ": £" + str(self.paid_amount)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return str(self.id)

    def get_total_price(self):
        return self.price