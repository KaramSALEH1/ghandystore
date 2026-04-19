from .models import Item

# item/cart.py

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_cart')
        if not cart:
            cart = self.session['session_cart'] = {}
        self.cart = cart

    def add(self, item):
        item_id = str(item.id)
        if item_id not in self.cart:
            image_url = item.image.url if getattr(item, 'image', None) else ''
            self.cart[item_id] = {
                'price': str(item.price),
                'qty': 1,
                'name': item.name,
                'image_url': image_url,
            }
        else:
            self.cart[item_id]['qty'] += 1
        self.session.modified = True

    def update(self, item_id, qty):
        item_id = str(item_id)
        if item_id not in self.cart:
            return
        if qty <= 0:
            self.remove(item_id)
            return
        self.cart[item_id]['qty'] = qty
        self.session.modified = True

    def remove(self, item_id):
        item_id = str(item_id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.session.modified = True

    def clear(self):
        self.session['session_cart'] = {}
        self.cart = self.session['session_cart']
        self.session.modified = True

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def __iter__(self):
        for item_id, data in self.cart.items():
            price = float(data['price'])
            qty = data['qty']
            item = Item.objects.filter(pk=item_id).first()
            if item:
                price = float(item.price)
                image_url = item.image.url if getattr(item, 'image', None) else data.get('image_url', '')
                name = item.name
                is_sold = item.is_sold
            else:
                image_url = data.get('image_url', '')
                name = data.get('name', '')
                is_sold = False
            yield {
                'id': item_id,
                'name': name,
                'price': price,
                'qty': qty,
                'line_total': price * qty,
                'image_url': image_url,
                'is_sold': is_sold,
            }

    def get_total_price(self):
        total = 0.0
        for item_id, data in self.cart.items():
            item = Item.objects.filter(pk=item_id).first()
            price = float(item.price) if item else float(data['price'])
            total += price * data['qty']
        return total