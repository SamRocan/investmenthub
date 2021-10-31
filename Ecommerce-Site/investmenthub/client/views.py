from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.contrib.auth import login
#from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response

from .charts import get_year_dict, generate_color_palette, generate_color_palette_boarder
from .models import Client
from product.models import Product
from product.forms import ProductForm
from .filters import UserProductFilter, OrderFilter

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            client = Client.objects.create(name=user.username, created_by=user)


            return redirect('homepage')
    else:
        form = UserCreationForm()
    return render(request, 'client/register.html', {'form':form})

@login_required
def client_admin(request):
    client = request.user.client
    products = client.products.all()
    noOfProducts = client.products.count()
    orders = client.orders.all()

    revenue = 0
    for order in orders:
        revenue += order.paid_amount

    noOfOrders = client.orders.count()
    ProductsFilter = UserProductFilter(request.GET, queryset=products)

    OrdersFilter = OrderFilter(request.GET, queryset=orders)


    products = ProductsFilter.qs
    #top 5 products
    orders = OrdersFilter.qs
    context = {
        'products':products,
        'productCount':noOfProducts,
        'orders':orders,
        'revenue':revenue,
        'orderCount':noOfOrders,
        'ProductsFilter':ProductsFilter,
        'OrdersFilter':OrdersFilter,
    }
    return render(request, 'client/client_admin.html', context)

class ChartData(APIView):

    def get(self, request, format = None):
        client = request.user.client
        orders = client.orders.all()
        dates = []
        paid = []
        for order in orders:
            if(str(order.created_at.date()) in dates):
                index = dates.index(str(order.created_at.date()))
                paid[index]+=int(order.paid_amount)
            else:
                dates.append(str(order.created_at.date()))
                paid.append(int(order.paid_amount))
        colorPalette = generate_color_palette(len(paid))
        colorPaletteBoarder = generate_color_palette_boarder(len(paid))
        data = {
            'colorPaletteBoarder':colorPaletteBoarder,
            'colorPalette':colorPalette,
            'dates':dates,
            'paid':paid
        }
        return Response(data)

@login_required
def add_product(request):
    if(request.method == 'POST'):
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.client = request.user.client
            product.slug = slugify(product.title)
            product.save()
            return redirect('client_admin')
    else:
        form = ProductForm()
    return render(request, 'client/add_product.html', {'form':form})

@login_required
def edit_product(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    form = ProductForm(instance=product)

    if(request.method == 'POST'):
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            product = form.save(commit=False)
            product.client = request.user.client
            product.slug = slugify(product.title)
            product.save()
            return redirect('client_admin')
        else:
            form = ProductForm(instance=product)


    return render(request, 'client/edit_product.html', {'form':form})

def delete_product(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    if request.method == 'POST':
        product.delete()
        return redirect('client_admin')

    return render(request, 'client/delete_product.html', {'item':product})


