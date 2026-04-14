import json
from pathlib import Path
from types import SimpleNamespace
from .models import Item
from .cart import Cart
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from urllib.parse import quote

from .forms import NewItemForm, EditItemForm, ItemRequestForm
from .models import Category, Item, City, Place, ItemColor

def add_to_cart(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    cart.add(item=item)
    
    # هذا السطر يعيد المستخدم لنفس الصفحة التي ضغط منها على الزر
    return redirect(request.META.get('HTTP_REFERER', '/'))

def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart_summary.html', {'cart': cart})


def _ns(value):
    if isinstance(value, dict):
        return SimpleNamespace(**{k: _ns(v) for k, v in value.items()})
    if isinstance(value, list):
        return [_ns(v) for v in value]
    return value


def _load_mock_json(filename: str):
    base_dir: Path = getattr(settings, 'MOCK_DATA_DIR', Path(settings.BASE_DIR) / 'mock-data')
    path = base_dir / filename
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def _mock_catalog():
    categories = _ns(_load_mock_json('categories.json'))
    items = _ns(_load_mock_json('items.json'))
    colors = _ns(_load_mock_json('item-colors.json'))
    return categories, items, colors


def category(request, pk ):
    if getattr(settings, 'USE_MOCK_DATA', False):
        categories, items, _colors = _mock_catalog()
        category_obj = next((c for c in categories if int(c.id) == int(pk)), None)
        page_items = [i for i in items if int(i.category_id) == int(pk) and not bool(getattr(i, 'is_sold', False))][0:9]
        return render(request, 'item/CategoryPage.html', {
            'items': page_items,
            'category': category_obj or SimpleNamespace(id=pk, name='Category'),
            'is_mock_data': True,
        })

    category = Category.objects.get(pk=pk)
    items = Item.objects.filter(category=category , is_sold=False)[0:9]

    return render(request, 'item/CategoryPage.html', {
        'items': items,
        'category': category,
    })


def detail(request, pk):
    if getattr(settings, 'USE_MOCK_DATA', False):
        categories, items, colors = _mock_catalog()
        item_obj = next((i for i in items if int(i.id) == int(pk)), None)
        if not item_obj:
            item_obj = SimpleNamespace(
                id=pk,
                name='Item',
                price='0',
                description='',
                category_id=1,
                image_url='https://picsum.photos/seed/ghandy-fallback/1200/900',
            )

        related_items = [i for i in items if int(i.category_id) == int(item_obj.category_id) and int(i.id) != int(pk) and not bool(getattr(i, 'is_sold', False))][0:3]

        item_colors = [c for c in colors if int(c.item_id) == int(item_obj.id)]
        item_colors = sorted(item_colors, key=lambda c: (c.name or '').lower())

        selected_color_id = request.GET.get('color', None)
        selected_color = next((c for c in item_colors if selected_color_id and str(c.id) == str(selected_color_id)), None)

        all_images = []
        selected_color_images = []
        if selected_color and not bool(getattr(selected_color, 'is_sold_out', False)):
            for img in getattr(selected_color, 'images', []) or []:
                selected_color_images.append({
                    'url': img.url,
                    'type': 'color',
                    'color': selected_color,
                    'color_id': selected_color.id,
                    'alt': getattr(img, 'alt', f"{item_obj.name} - {selected_color.name}"),
                })

        if getattr(item_obj, 'image_url', None) and (not selected_color or not selected_color_images):
            all_images.append({
                'url': item_obj.image_url,
                'type': 'main',
                'color': None,
                'color_id': None,
                'alt': f"{item_obj.name} - Main Image",
            })

        all_images.extend(selected_color_images)

        for c in item_colors:
            if bool(getattr(c, 'is_sold_out', False)) or c == selected_color:
                continue
            for img in getattr(c, 'images', []) or []:
                all_images.append({
                    'url': img.url,
                    'type': 'color',
                    'color': c,
                    'color_id': c.id,
                    'alt': getattr(img, 'alt', f"{item_obj.name} - {c.name}"),
                })

        return render(request, 'item/ProductDetailPage.html', {
            'item': item_obj,
            'related_items': related_items,
            'colors': item_colors,
            'selected_color': selected_color,
            'all_images': all_images,
            'show_form': False,
            'is_mock_data': True,
        })

    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    
    # Get all colors for this item with their images
    colors = ItemColor.objects.filter(item=item).prefetch_related('images').order_by('name')
    
    # Get selected color from request (for displaying specific color images)
    selected_color_id = request.GET.get('color', None)
    selected_color = None
    if selected_color_id:
        try:
            selected_color = ItemColor.objects.get(pk=selected_color_id, item=item)
        except ItemColor.DoesNotExist:
            selected_color = None
    
    # Collect all images: main item image first, then all color images
    # If a color is selected, put that color's images first
    all_images = []
    selected_color_images = []
    
    # If color is selected, collect its images first
    if selected_color and not selected_color.is_sold_out:
        for color_image in selected_color.images.all():
            selected_color_images.append({
                'url': color_image.image.url,
                'type': 'color',
                'color': selected_color,
                'color_id': selected_color.id,
                'alt': f"{item.name} - {selected_color.name}"
            })
    
    # Add main item image (only if no color selected or color has no images)
    if item.image and (not selected_color or not selected_color_images):
        all_images.append({
            'url': item.image.url,
            'type': 'main',
            'color': None,
            'color_id': None,
            'alt': f"{item.name} - Main Image"
        })
    
    # Add selected color images first if they exist
    all_images.extend(selected_color_images)
    
    # Add other color images (excluding selected color if it was added above)
    for color in colors:
        if not color.is_sold_out and color != selected_color:
            for color_image in color.images.all():
                all_images.append({
                    'url': color_image.image.url,
                    'type': 'color',
                    'color': color,
                    'color_id': color.id,
                    'alt': f"{item.name} - {color.name}"
                })

    form = ItemRequestForm(item=item)
    show_form = False
    
    if request.method == 'POST':
        form = ItemRequestForm(request.POST, item=item)
        # Check for color in POST data or GET parameter
        color_id_from_post = form.data.get('color')
        color_id_from_get = request.GET.get('color')
        color_id_to_use = color_id_from_post or color_id_from_get
        
        # If form has a color selected (even if invalid), use it for display
        if color_id_to_use:
            try:
                color_id = int(color_id_to_use)
                selected_color = ItemColor.objects.filter(pk=color_id, item=item).first()
                # Rebuild images list with selected color first
                if selected_color:
                    all_images = []
                    selected_color_images = []
                    if not selected_color.is_sold_out:
                        for color_image in selected_color.images.all():
                            selected_color_images.append({
                                'url': color_image.image.url,
                                'type': 'color',
                                'color': selected_color,
                                'color_id': selected_color.id,
                                'alt': f"{item.name} - {selected_color.name}"
                            })
                    if item.image and not selected_color_images:
                        all_images.append({
                            'url': item.image.url,
                            'type': 'main',
                            'color': None,
                            'color_id': None,
                            'alt': f"{item.name} - Main Image"
                        })
                    all_images.extend(selected_color_images)
                    for color in colors:
                        if not color.is_sold_out and color != selected_color:
                            for color_image in color.images.all():
                                all_images.append({
                                    'url': color_image.image.url,
                                    'type': 'color',
                                    'color': color,
                                    'color_id': color.id,
                                    'alt': f"{item.name} - {color.name}"
                                })
            except (ValueError, TypeError):
                pass
        if form.is_valid():
            # Save the request to database
            item_request = form.save(commit=False)
            item_request.item = item
            item_request.save()
            
            # Build WhatsApp message
            customer_name = form.cleaned_data['customer_name']
            customer_phone = form.cleaned_data['customer_phone']
            color = form.cleaned_data.get('color')
            city = form.cleaned_data.get('city')
            place = form.cleaned_data.get('place')
            
            whatsapp_message = f"Hello! I'm interested in purchasing:\n\n"
            whatsapp_message += f"Item: {item.name}\n"
            if color:
                whatsapp_message += f"Color: {color.name}\n"
            whatsapp_message += f"Price: {item.price}\n"
            if item.description:
                whatsapp_message += f"Description: {item.description}\n"
            whatsapp_message += f"\nMy Information:\n"
            whatsapp_message += f"Name: {customer_name}\n"
            whatsapp_message += f"Phone: {customer_phone}\n"
            if city:
                whatsapp_message += f"City: {city.name}\n"
            if place:
                whatsapp_message += f"Place of Delivery: {place.name}\n"
            
            # Encode message for URL
            encoded_message = quote(whatsapp_message)
            whatsapp_url = f"https://wa.me/+963937341881?text={encoded_message}"
            
            # Redirect to WhatsApp
            return redirect(whatsapp_url)
        else:
            # Form has errors, show the form
            show_form = True
            # Preserve selected color in form initial data and ensure it's in the context
            if selected_color:
                form.fields['color'].initial = selected_color.id
                # Also rebuild images list to show selected color first
                all_images = []
                selected_color_images = []
                if not selected_color.is_sold_out:
                    for color_image in selected_color.images.all():
                        selected_color_images.append({
                            'url': color_image.image.url,
                            'type': 'color',
                            'color': selected_color,
                            'color_id': selected_color.id,
                            'alt': f"{item.name} - {selected_color.name}"
                        })
                if item.image and not selected_color_images:
                    all_images.append({
                        'url': item.image.url,
                        'type': 'main',
                        'color': None,
                        'color_id': None,
                        'alt': f"{item.name} - Main Image"
                    })
                all_images.extend(selected_color_images)
                for color in colors:
                    if not color.is_sold_out and color != selected_color:
                        for color_image in color.images.all():
                            all_images.append({
                                'url': color_image.image.url,
                                'type': 'color',
                                'color': color,
                                'color_id': color.id,
                                'alt': f"{item.name} - {color.name}"
                            })

    return render(request, 'item/ProductDetailPage.html', {
        'item': item,
        'related_items': related_items,
        'colors': colors,
        'selected_color': selected_color,
        'all_images': all_images,
        'form': form,
        'show_form': show_form
    })

def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    if getattr(settings, 'USE_MOCK_DATA', False):
        categories, items, _colors = _mock_catalog()
        filtered_items = [i for i in items if not bool(getattr(i, 'is_sold', False))]

        if category_id:
            filtered_items = [i for i in filtered_items if int(i.category_id) == int(category_id)]

        if query:
            q = query.lower().strip()
            filtered_items = [
                i for i in filtered_items
                if q in (getattr(i, 'name', '') or '').lower() or q in (getattr(i, 'description', '') or '').lower()
            ]

        return render(request, 'item/ProductListingPage.html', {
            'items': filtered_items,
            'query': query,
            'categories': categories,
            'category_id': int(category_id) if category_id else 0,
            'is_mock_data': True,
        })

    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'item/ProductListingPage.html', {
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

def get_places_by_city(request, city_id):
    """API endpoint to fetch places for a given city"""
    places = Place.objects.filter(city_id=city_id).order_by('name')
    places_data = [{'id': place.id, 'name': place.name} for place in places]
    return JsonResponse({'places': places_data})