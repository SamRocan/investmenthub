from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import JsonResponse
from .cart import Cart

from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings

# Create your views here.
def cart_detail(request):
    cart = Cart(request)
    remove_from_cart = request.GET.get('remove_from_cart', '')
    if remove_from_cart:
        cart.remove(remove_from_cart)
        return redirect('cart')

    return render(request, 'cart/cart.html',)

class OrderCompleted(View):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        #Send Email from here
        current_user = request.user
        send_email(cart, current_user.email)
        print(current_user.email)
        cart.clear()
        context = {
        }
        return JsonResponse(context, safe=False)


def send_email(cart, email):
    for i in cart:
        file = i['product'].file.path
        email = EmailMessage(
            str(i['product'].title)+': Ready to Download',
            'Thank you for purchasing ' + str(i['product'].title) + 'please find you file attached',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            reply_to=[settings.DEFAULT_FROM_EMAIL],
            headers={'Message-ID': 'foo'},
        )
        email.attach_file(file)
        email.send()