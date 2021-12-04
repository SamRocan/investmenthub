from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.contrib.auth import login
#from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from datetime import date

from rest_framework.views import APIView
from rest_framework.response import Response

from .charts import currentDaysOfYear, getDateRange, getSoldCountAndRevenue, getProductAddedCount, generate_color_palette, generate_color_palette_boarder
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
def client_products(request, page=1):
    client = request.user.client
    products = client.products.all()
    ProductsFilter = UserProductFilter(request.GET, queryset=products)

    paginator = Paginator(ProductsFilter.qs, 3)
    try:
        products = paginator.page(page)
    except EmptyPage:
        # if we exceed the page limit we return the last page
        products = paginator.page(paginator.num_pages)

    return render(request, 'client/client_products.html', {'products':products,
                                                           'ProductsFilter':ProductsFilter})
@login_required
def client_orders(request, page=1):
    client = request.user.client
    orders = client.orders.all()
    OrdersFilter = OrderFilter(request.GET, queryset=orders)

    paginator = Paginator(OrdersFilter.qs, 3)
    try:
        orders = paginator.page(page)
    except EmptyPage:
    # if we exceed the page limit we return the last page
        orders = paginator.page(paginator.num_pages)
    return render(request, 'client/client_orders.html', {'orders':orders,
                                                         'OrdersFilter':OrdersFilter})


@login_required
def client_admin(request):
    client = request.user.client
    products = client.products.all()
    noOfProducts = client.products.count()
    orders = client.orders.all()
    items = client.items.all()
    revenue = 0
    for order in orders:
        revenue += order.paid_amount

    noOfOrders = client.orders.count()
    ProductsFilter = UserProductFilter(request.GET, queryset=products)

    OrdersFilter = OrderFilter(request.GET, queryset=orders)


    #top 5 products
    mostPop = {}
    for product in products:
        mostPop[product.title] = 0

    for item in items:
        mostPop[item.product.title] += 1

    productsSorted = {k: v for k, v in sorted(mostPop.items(), reverse=True, key=lambda x: x[1])}
    print(len(productsSorted))
    if(len(productsSorted)!=0):
        mostPopProduct = list(productsSorted.keys())[0]
        mostPopProduct = mostPopProduct[0:20]
        mostPopProduct = mostPopProduct[0:mostPopProduct.rfind(" ")]+" ..."
    else:
        mostPopProduct="N/A"
    soldCount = orders.count
    revenueCount= revenue
    addedCount = products.count
    if(len(OrdersFilter.data)!=0):
        dateRange = OrdersFilter.data['date_range']
        if dateRange == 'today':
            soldCount = 0
            revenueCount = 0
            addedCount = 0
            for i in orders:
                if(i.created_at.date() == date.today()):
                    soldCount+=1
                    revenueCount+=i.paid_amount
            for i in products:
                if(i.date_added.date() == date.today()):
                    addedCount+=1
        if dateRange == 'yesterday':
            rng = getDateRange(2)
            sr = getSoldCountAndRevenue(orders, rng)
            soldCount = sr[0]
            revenueCount = sr[1]
            addedCount = getProductAddedCount(products, rng)
        if dateRange == 'week':
            rng = getDateRange(7)
            sr = getSoldCountAndRevenue(orders, rng)
            soldCount = sr[0]
            revenueCount = sr[1]
            addedCount = getProductAddedCount(products, rng)
        if dateRange == 'month':
            rng = getDateRange(30)
            sr = getSoldCountAndRevenue(orders, rng)
            soldCount = sr[0]
            revenueCount = sr[1]
            addedCount = getProductAddedCount(products, rng)
        if dateRange == 'year':
            rng = getDateRange(365)
            sr = getSoldCountAndRevenue(orders, rng)
            soldCount = sr[0]
            revenueCount = sr[1]
            addedCount = getProductAddedCount(products, rng)

        request.session['token'] = dateRange
    context = {
        'products':products,
        'productCount':noOfProducts,
        'productsSorted':productsSorted,
        'mostPopProduct':mostPopProduct,
        'orders':orders,
        'revenue':revenue,
        'orderCount':noOfOrders,
        'ProductsFilter':ProductsFilter,
        'OrdersFilter':OrdersFilter,
        'soldCount':soldCount,
        'revenueCount':revenueCount,
        'addedCount':addedCount
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

@login_required
def delete_product(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    if request.method == 'POST':
        product.delete()
        return redirect('client_admin')

    return render(request, 'client/delete_product.html', {'item':product})


