from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import JsonResponse
from .cart import Cart

# Create your views here.
def cart_detail(request):
    cart = Cart(request)

    remove_from_cart = request.GET.get('remove_from_cart', '')
    if remove_from_cart:
        cart.remove(remove_from_cart)
        return redirect('cart')

    return render(request, 'cart/cart.html',)

class OrderCompleted(View):
    def get(self,request, *args, **kwargs):
        cart = Cart(request)
        cart.clear()
        context = {
        }
        return JsonResponse(context, safe=False)
