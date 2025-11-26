from django.shortcuts import render, redirect
from item.models import Category, Item
from .forms import SignupForm

def index(request):
    items = Item.objects.filter(is_sold=False)[0:9]
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

