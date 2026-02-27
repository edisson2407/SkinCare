def cart_context(request):
    """Context processor que expone la cantidad total de items en el carrito.

    Devuelve `cart_count` para usar en las plantillas.
    """
    cart = request.session.get("cart", {"items": []})
    try:
        qty = sum(int(i.get("cantidad", 1)) for i in cart.get("items", []))
    except Exception:
        qty = 0
    return {"cart_count": qty}
