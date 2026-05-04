from .models import Item, ItemColor

# item/cart.py

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_cart')
        if not cart:
            cart = self.session['session_cart'] = {}
        self.cart = cart

    def _make_line_id(self, item_id: int, color_id: int, size: str | None = None) -> str:
        if size:
            return f"{item_id}:{color_id}:{size}"
        return f"{item_id}:{color_id}"

    def _parse_line_id(self, line_id: str):
        parts = str(line_id).split(":")
        item_id = parts[0] if len(parts) >= 1 else None
        color_id = parts[1] if len(parts) >= 2 else None
        size = ":".join(parts[2:]) if len(parts) >= 3 else None
        return item_id, color_id, size

    def add(self, item, color: ItemColor, size: str | None = None):
        if not color:
            return
        line_id = self._make_line_id(item.id, color.id, size=size)
        if line_id not in self.cart:
            self.cart[line_id] = {
                'item_id': str(item.id),
                'color_id': str(color.id),
                'color_name': color.name,
                'size': (str(size) if size else ''),
                'price': str(item.price),
                'qty': 1,
                'name': item.name,
                'image_url': getattr(item, 'image_url', '') or '',
            }
        else:
            self.cart[line_id]['qty'] += 1
        self.session.modified = True

    def update(self, line_id, qty):
        line_id = str(line_id)
        if line_id not in self.cart:
            return
        if qty <= 0:
            self.remove(line_id)
            return
        self.cart[line_id]['qty'] = qty
        self.session.modified = True

    def remove(self, line_id):
        line_id = str(line_id)
        if line_id in self.cart:
            del self.cart[line_id]
            self.session.modified = True

    def clear(self):
        self.session['session_cart'] = {}
        self.cart = self.session['session_cart']
        self.session.modified = True

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def __iter__(self):
        for line_id, data in list(self.cart.items()):
            qty = data.get('qty', 0) or 0
            raw_price = data.get('price', '0') or '0'
            try:
                price = float(raw_price)
            except (TypeError, ValueError):
                price = 0.0

            item_id = data.get('item_id')
            color_id = data.get('color_id')
            size = data.get('size') or None

            if not item_id:
                parsed_item_id, parsed_color_id, parsed_size = self._parse_line_id(line_id)
                item_id = parsed_item_id
                color_id = color_id or parsed_color_id
                size = size or parsed_size

                data['item_id'] = str(item_id)
                if color_id:
                    data['color_id'] = str(color_id)
                if size is not None:
                    data['size'] = str(size)
                self.session.modified = True

            try:
                item_pk = int(item_id)
            except (TypeError, ValueError):
                self.cart.pop(line_id, None)
                self.session.modified = True
                continue

            item = Item.objects.filter(pk=item_pk).first()
            color = None
            if item and color_id:
                color = ItemColor.objects.filter(pk=color_id, item=item).first()
            if item:
                price = float(item.price)
                image_url = getattr(item, 'image_url', '') or ''
                name = item.name
                is_sold = item.is_sold
            else:
                image_url = data.get('image_url', '')
                name = data.get('name', '')
                is_sold = False
            yield {
                'id': item.id if item else item_pk,
                'line_id': line_id,
                'name': name,
                'color_id': color.id if color else None,
                'color_name': color.name if color else (data.get('color_name', '') or ''),
                'size': size or '',
                'price': price,
                'qty': qty,
                'line_total': price * qty,
                'image_url': image_url,
                'is_sold': is_sold,
            }

    def get_total_price(self):
        total = 0.0
        for line_id, data in self.cart.items():
            qty = data.get('qty', 0) or 0

            item_id = data.get('item_id')
            if not item_id:
                if ':' in str(line_id):
                    item_id = str(line_id).split(':', 1)[0]
                else:
                    item_id = str(line_id)

            try:
                item_pk = int(item_id)
            except (TypeError, ValueError):
                continue

            item = Item.objects.filter(pk=item_pk).first()
            raw_price = data.get('price', '0') or '0'
            try:
                fallback_price = float(raw_price)
            except (TypeError, ValueError):
                fallback_price = 0.0

            unit_price = float(item.price) if item else fallback_price
            total += unit_price * qty
        return total
