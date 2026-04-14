# item/context_processors.py
from item.cart import Cart

def cart(request):
    return {'global_cart': Cart(request)}