from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from urllib.parse import quote

from .forms import NewItemForm, EditItemForm, ItemRequestForm
from .models import Category, Item


def category(request, pk ):
    category= Category.objects.get(pk=pk)
    item = Item.objects.filter(category=category , is_sold=False).exclude(pk=pk)[0:9]

    return render(request, 'item/category.html',{
        'item': item,
        'category': category,
    })


def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    form = ItemRequestForm()
    show_form = False
    
    if request.method == 'POST':
        form = ItemRequestForm(request.POST)
        if form.is_valid():
            # Save the request to database
            item_request = form.save(commit=False)
            item_request.item = item
            item_request.save()
            
            # Build WhatsApp message
            customer_name = form.cleaned_data['customer_name']
            customer_phone = form.cleaned_data['customer_phone']
            message = form.cleaned_data.get('message', '')
            
            whatsapp_message = f"Hello! I'm interested in purchasing:\n\n"
            whatsapp_message += f"Item: {item.name}\n"
            whatsapp_message += f"Price: {item.price}\n"
            if item.description:
                whatsapp_message += f"Description: {item.description}\n"
            whatsapp_message += f"\nMy Information:\n"
            whatsapp_message += f"Name: {customer_name}\n"
            whatsapp_message += f"Phone: {customer_phone}\n"
            if message:
                whatsapp_message += f"\nMessage: {message}\n"
            
            # Encode message for URL
            encoded_message = quote(whatsapp_message)
            whatsapp_url = f"https://wa.me/+963937341881?text={encoded_message}"
            
            # Redirect to WhatsApp
            return redirect(whatsapp_url)
        else:
            # Form has errors, show the form
            show_form = True

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items,
        'form': form,
        'show_form': show_form
    })

def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })


@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('base:index')