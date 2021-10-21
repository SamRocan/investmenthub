from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
# Create your views here.

from .models import Product
from client.filters import ProductFilter, BasicProductFilter
from cart.cart import Cart

def product_home(request):
    colors = {
        "Horizontal Analysis":"rgba(180, 8, 8, 0.1)",
        "Vertical Analysis":"rgba(248, 152, 42, 0.1)",
        "Trend Analysis":"rgba(247, 221, 53, 0.1)",
        "Liquidity Analysis":"rgba(43, 186, 7, 0.1)",
        "Solvency Analysis":"rgba(7, 186, 135, 0.1)",
        "Profitability Analysis":"rgba(7, 96, 186, 0.1)",
        "Scenario & Sensitivity Analysis":"rgba(96, 7, 186, 0.1)",
        "Variance Analysis":"rgba(186, 7, 180, 0.1)",
        "Valuation Analysis":"rgba(186, 7, 43, 0.1)",
        "FP&A Analysis":"rgba(153, 153, 153, 0.1)",
    }
    products = Product.objects.all()
    if request.method == "POST":
        prodQuery = request.POST["product_searcher"]
        products = Product.objects.filter(title__contains=prodQuery)
        myFilter = ProductFilter(request.GET, queryset=products)
    else:
        myFilter = ProductFilter(request.GET, queryset=products)
        products = myFilter.qs
    return render(request, 'product/product_search.html', {'products':products, 'myFilter':myFilter, 'colors':colors})

def product_page(request, product_slug):
    cart = Cart(request)

    product = get_object_or_404(Product, slug=product_slug)
    if request.method == 'POST':
        cart.add(product_id=product.id, quantity=1)
        print("Added")
        return redirect('product_page', product_slug=product_slug)


    return render(request, 'product/product_page.html', {'product':product})