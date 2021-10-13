from django.shortcuts import render, redirect
from .cart import Cart

# Create your views here.
def cart_detail(request):
    cart = Cart(request)

    remove_from_cart = request.GET.get('remove_from_cart', '')
    if remove_from_cart:
        print("ERROR")
        cart.remove(remove_from_cart)
        return redirect('cart')

    return render(request, 'cart/cart.html',)