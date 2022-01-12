from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from cart.cart import Cart

from .models import Order, OrderItem

def checkout(request, first_name, last_name, email, amount):
    '''
    Creates an order object from items in the cart
    :param first_name: str
    :param last_name: str
    :param email: str
    :param amount: float
    :return: Order Model Instance
    '''
    order = Order.objects.create(first_name=first_name, last_name=last_name, email=email, paid_amount=amount)

    for item in Cart(request):
        OrderItem.objects.create(order=order, product=item['product'], client=item['product'].client, price=item['product'].price)

        order.client.add(item['product'].client)

    return order