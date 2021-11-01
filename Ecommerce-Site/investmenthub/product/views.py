from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

from .models import Product
from order.models import OrderItem
from client.filters import ProductFilter, BasicProductFilter
from cart.cart import Cart

def product_home(request):
    products = Product.objects.all()
    if request.method == "GET":
        prodQuery = request.GET.get('product_searcher')
        products = Product.objects.filter(title__contains=prodQuery)
        myFilter = ProductFilter(request.GET, queryset=products)
    else:
        myFilter = ProductFilter(request.GET, queryset=products)
        products = myFilter.qs

    context = {
        'products':products,
        'myFilter':myFilter,
    }
    return render(request, 'product/product_search.html', context)

def product_page(request, product_slug):
    cart = Cart(request)

    product = get_object_or_404(Product, slug=product_slug)
    if request.method == 'POST':
        cart.add(product_id=product.id, quantity=1)
        print("Added")
        return redirect('product_page', product_slug=product_slug)


    return render(request, 'product/product_page.html', {'product':product})