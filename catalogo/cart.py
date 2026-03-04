from decimal import Decimal
from django.conf import settings

class Cart:
    SESSION_KEY = "cart"

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(self.SESSION_KEY)
        if cart is None:
            cart = {"items": []}
        self.cart = cart

    def save(self):
        self.session[self.SESSION_KEY] = self.cart
        self.session.modified = True

    def add(self, producto_id, nombre, precio, cantidad=1):
        precio = float(precio)
        for item in self.cart["items"]:
            if item["id"] == producto_id:
                item["cantidad"] += cantidad
                self.save()
                return
        self.cart["items"].append({
            "id": producto_id,
            "nombre": nombre,
            "precio": precio,
            "cantidad": cantidad
        })
        self.save()

    def update(self, producto_id, cantidad):
        for item in self.cart["items"]:
            if item["id"] == producto_id:
                item["cantidad"] = max(1, cantidad)
                break
        self.save()

    def remove(self, producto_id):
        self.cart["items"] = [i for i in self.cart["items"] if i["id"] != producto_id]
        self.save()

    def items(self):
        return self.cart["items"]

    def total(self):
        return float(sum(i["precio"] * i["cantidad"] for i in self.cart["items"]))
    
    def get_qty(self, producto_id):
        for item in self.cart["items"]:
            if item["id"] == producto_id:
                return int(item["cantidad"])
        return 0
