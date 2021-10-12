from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from .models import Product
from client.filters import ProductFilter
def product_home(request):
    products = Product.objects.all()
    myFilter = ProductFilter(request.GET, queryset=products)

    products = myFilter.qs
    return render(request, 'product/product_home.html', {'products':products, 'myFilter':myFilter})

