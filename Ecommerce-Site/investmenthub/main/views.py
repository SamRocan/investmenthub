from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from cart.cart import Cart

# Create your views here.s
def homepage(request):
    return render(request, 'main/homepage.html')
