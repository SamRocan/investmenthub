from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.contrib.auth import login
#from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage



from rest_framework.views import APIView
from rest_framework.response import Response

from .charts import currentDaysOfYear, generate_color_palette, generate_color_palette_boarder
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

def client_products(request, page=1):
    client = request.user.client
    products = client.products.all()
    paginator = Paginator(products, 3)

    try:
        products = paginator.page(page)
    except EmptyPage:
        # if we exceed the page limit we return the last page
        products = paginator.page(paginator.num_pages)

    return render(request, 'client/client_products.html', {'products':products})

def client_orders(request, page=1):
    client = request.user.client
    orders = client.orders.all()
    paginator = Paginator(orders, 3)

    try:
        orders = paginator.page(page)
    except EmptyPage:
    # if we exceed the page limit we return the last page
        orders = paginator.page(paginator.num_pages)
    return render(request, 'client/client_orders.html', {'orders':orders})


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


    #products = ProductsFilter.qs
    #top 5 products
    #orders = OrdersFilter.qs
    if(len(OrdersFilter.data)!=0):
        dateRange = OrdersFilter.data['date_range']
        request.session['token'] = dateRange
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
        dateRange = request.session['token']
        items = client.items.all()
        itemAdded = []
        itemCount = []
        for i in items:
            if(i.product.title in itemAdded):
                x = itemAdded.index(i.product.title)
                itemCount[x] +=1
            else:
                itemAdded.append(i.product.title[0:20]+"...")
                itemCount.append(1)


        total = 0
        dates = currentDaysOfYear()
        for order in orders:
            if(str(order.created_at.date()) in dates.keys()):
                dates[str(order.created_at.date())] += int(order.paid_amount)
                total += 1

        dr = 30
        if dateRange == 'today':
            dr=1
        elif dateRange == 'yesterday':
            dr=2
        elif dateRange == 'week':
            dr=7
        elif dateRange == 'month':
            dr=30
        elif dateRange == 'year':
            dr=365
        paid = list(dates.values())[-dr:]
        dates = list(dates.keys())[-dr:]
        colorPalette = generate_color_palette(total)
        colorPaletteBoarder = generate_color_palette_boarder(total)
        data = {
            'colorPaletteBoarder':colorPaletteBoarder,
            'colorPalette':colorPalette,
            'dates':dates,
            'paid':paid,
            'product':itemAdded,
            'productCount':itemCount,
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


    return render(request, 'client/edit_product.html', {'form':form, 'product':product})

def delete_product(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    if request.method == 'POST':
        product.delete()
        return redirect('client_admin')

    return render(request, 'client/delete_product.html', {'item':product})


