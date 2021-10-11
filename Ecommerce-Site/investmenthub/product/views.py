from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from .models import Product
def product_home(request):
    products = Product.objects.all()
    print(products[0].title)
    return render(request, 'product/product_home.html', {'products':products})

