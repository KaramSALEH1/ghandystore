from django.conf import settings
from django.shortcuts import render, redirect
from item.cart import Cart
from item.models import Category, Item, City
from .forms import SignupForm

def index(request):
    items = Item.objects.all().order_by('-created_at')[0:9]
    categories = Category.objects.all()

    return render(request, 'base/index.html', {
        'categories': categories,
        'items': items,
    })

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'base/signup.html', {
        'form': form
    })


def checkout(request):
    cart = Cart(request)
    cart_has_sold = any(getattr(line, 'is_sold', False) for line in cart)
    return render(request, 'base/checkout.html', {
        'whatsapp_order_number': getattr(settings, 'WHATSAPP_ORDER_NUMBER', '963937341881'),
        'cart_has_sold': cart_has_sold,
        'cities': City.objects.prefetch_related('places').all(),
    })

