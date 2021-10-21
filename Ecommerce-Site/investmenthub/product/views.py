from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
# Create your views here.

from .models import Product
from client.filters import ProductFilter, BasicProductFilter
from cart.cart import Cart

def product_home(request):
    products = Product.objects.all()
    if request.method == "POST":
        prodQuery = request.POST["product_searcher"]
        print(prodQuery)
        products = Product.objects.filter(title__contains=prodQuery)
        myFilter = ProductFilter(request.GET, queryset=products)
    else:
        myFilter = ProductFilter(request.GET, queryset=products)
        products = myFilter.qs
    return render(request, 'product/product_search.html', {'products':products, 'myFilter':myFilter})

def product_page(request, product_slug):
    cart = Cart(request)

    product = get_object_or_404(Product, slug=product_slug)
    if request.method == 'POST':
        cart.add(product_id=product.id, quantity=1)
        print("Added")
        return redirect('product_page', product_slug=product_slug)


    return render(request, 'product/product_page.html', {'product':product})