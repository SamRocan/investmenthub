from django.conf import settings

from product.models import Product

class Cart(object):
    '''
    A Cart to hold all products selected by the user for purchase.

    Attributes
    ----------
    session : session
        a django session to hold all product items for purchase

    cart :  session
        a django session to hold all product items for purchase

    Methods
    -------
    add(self, product_id, quantity)
        Adds a ProductItem model instance to the cart

    remove(self, product_id)
        Removes a ProductItem model instance from the cart

    save(self)
        Saves the cart data to a django session

    clear(self)
        Clears the cart data from the django session

    get_total_cost(self)
        Calculates the total value of cart from the product price
    '''

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart


    def __iter__(self):
        '''
        Returns a generator givinng the total value of all items in cart
        :return: item: generator
        '''
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)

        for item in self.cart.values():
            item['total_price'] = item['product'].price * item['quantity']

            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product_id, quantity=1):
        '''
        Adds a ProductItem model instance to the cart
        :param product_id: it
        :param quantity: int
        :return:
        '''
        product_id = str(product_id)

        if(product_id not in self.cart):
            self.cart[product_id] = {'quantity':1, 'id':product_id}

        self.save()

    def remove(self, product_id):
        '''
        Removes a ProductItem model instance from the cart
        :param product_id: int
        :return:
        '''
        if(product_id in self.cart):
            del self.cart[product_id]
            self.save()

    def save(self):
        '''
        Saves the cart data to a django session
        :return:
        '''
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def clear(self):
        '''
        Clears the cart data from the django session
        :return:
        '''
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_cost(self):
        '''
        Calculates the total value of cart from the product price
        :return: total: int
            returns the total price of all items i the cart
        '''
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)

        return sum(item['quantity'] * item['product'].price for item in self.cart.values())