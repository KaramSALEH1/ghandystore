from django.conf import settings
from item.cart import Cart
from item.models import Category

def cart(request):
    return {
        'global_cart': Cart(request),
        'global_categories': Category.objects.all(),
        'global_whatsapp_number': getattr(settings, 'WHATSAPP_ORDER_NUMBER', ''),
        'global_instagram_url': getattr(settings, 'INSTAGRAM_URL', ''),
    }
