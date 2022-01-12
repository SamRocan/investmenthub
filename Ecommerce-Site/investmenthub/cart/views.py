from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import JsonResponse
from .cart import Cart
from order.utilities import checkout

from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings

# Create your views here.
def cart_detail(request):
    # https://developer.paypal.com/developer/creditCardGenerator/
    cart = Cart(request)
    remove_from_cart = request.GET.get('remove_from_cart', '')
    if remove_from_cart:
        cart.remove(remove_from_cart)
        return redirect('cart')

    return render(request, 'cart/cart.html',)

class OrderCompleted(View):
    def get(self, request, *args, **kwargs):
        print("Running")
        cart = Cart(request)
        print("Running2")
        #Send Email from here
        current_user = request.user
        print("Running3")

        # Uncomment when you want to notify the sellers
        '''
        notify_buyer(cart, current_user.email)
        print("Running4")
        notify_seller(cart)'''

        print(current_user.email)
        checkout(request, current_user.first_name, current_user.last_name, current_user.email, cart.get_total_cost())
        print("Running5")
        cart.clear()
        print("Running6")
        context = {
        }
        return JsonResponse(context, safe=False)

#Create functions here to notify the seller,  and create orders

def notify_seller(cart):
    '''
    Sends an email to the Seller of the product notifying him of his sale and the details
    regarding it
    :param cart: Cart
    :return:
    '''
    for i in cart:
        seller_email = i['product'].client.created_by.email
        email = EmailMessage(
            'Item Sold: ' + str(i['product'].title),
            str(i['product'].title) + 'Has been purchased, £'+str(i['product'].price) + ' has been transferred to your Paypal Account.',
            settings.DEFAULT_FROM_EMAIL,
            [seller_email],
            reply_to=[settings.DEFAULT_FROM_EMAIL],
            headers={'Message-ID': 'foo'},
        )
        email.send()

def notify_buyer(cart, buyer_email):
    '''
    Sends an email to the buyer of the product notifying him of his purchase and the details
    regarding it
    :param cart: Cart
    :param buyer_email: str
    :return:
    '''
    for i in cart:
        file = i['product'].file.path
        email = EmailMessage(
            str(i['product'].title)+': Ready to Download',
            'Thank you for purchasing ' + str(i['product'].title) + '. Please find you file attached',
            settings.DEFAULT_FROM_EMAIL,
            [buyer_email],
            reply_to=[settings.DEFAULT_FROM_EMAIL],
            headers={'Message-ID': 'foo'},
        )
        email.attach_file(file)
        email.send()