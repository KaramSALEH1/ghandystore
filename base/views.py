import json
from pathlib import Path
from types import SimpleNamespace

from django.conf import settings
from django.shortcuts import render, redirect
from item.models import Category, Item
from .forms import SignupForm


def _ns(value):
    if isinstance(value, dict):
        return SimpleNamespace(**{k: _ns(v) for k, v in value.items()})
    if isinstance(value, list):
        return [_ns(v) for v in value]
    return value


def _load_mock_json(filename: str):
    base_dir: Path = getattr(settings, 'MOCK_DATA_DIR', Path(settings.BASE_DIR) / 'mock-data')
    with (base_dir / filename).open('r', encoding='utf-8') as f:
        return json.load(f)

def index(request):
    if getattr(settings, 'USE_MOCK_DATA', False):
        items = _ns(_load_mock_json('items.json'))[0:9]
        categories = _ns(_load_mock_json('categories.json'))
        return render(request, 'base/index.html', {
            'categories': categories,
            'items': items,
            'is_mock_data': True,
        })

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


def checkout(request):
    return render(request, 'base/checkout.html')

