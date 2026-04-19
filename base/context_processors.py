# item/context_processors.py
from item.cart import Cart
from item.models import Category

def cart(request):
    return {
        'global_cart': Cart(request),
        'global_categories': Category.objects.all(),
    }