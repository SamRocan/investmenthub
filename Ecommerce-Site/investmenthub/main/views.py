from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from cart.cart import Cart
from product.models import Product
from order.models import OrderItem
# Create your views here.s
def homepage(request):
    newProducts = Product.objects.order_by('date_added')[0:5]
    orderItems = OrderItem.objects.all()

    mostPopular = {}
    for item in orderItems:
        if(item.product.title not in mostPopular.keys()):
            mostPopular[item.product.title] = 1
        else:
            mostPopular[item.product.title] += 1

    sorted(mostPopular, key=mostPopular.get)
    if len(mostPopular.keys()) > 5:
        mostPopularProducts = mostPopular.keys()[0:5]
    else:
        mostPopularProducts = mostPopular.keys()
    context = {
        'newProducts':newProducts,
        'mostPopularProducts':mostPopularProducts,
    }
    return render(request, 'main/homepage.html', context)
