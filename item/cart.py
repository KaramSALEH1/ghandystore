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
            self.cart[item_id] = {'price': str(item.price), 'qty': 1, 'name': item.name}
        else:
            self.cart[item_id]['qty'] += 1
        self.session.modified = True

    def get_total_price(self):
        # تأكد من تحويل السعر لرقم عشري أو صحيح قبل الجمع
        return sum(float(item['price']) * item['qty'] for item in self.cart.values())