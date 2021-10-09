from django.db import models
from client.models import Client
# Create your models here.

class ResearchType(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=255)
    research_type = models.ForeignKey(ResearchType, related_name='products', default=0, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='products', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    #image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    #thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title