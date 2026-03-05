from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseBadRequest
from django.conf import settings
from urllib.parse import quote
from django.contrib import messages
from django.shortcuts import redirect
from urllib.parse import quote
from decimal import Decimal
from .models import Producto
from .cart import Cart
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect, get_object_or_404

from .models import Producto, Categoria, Marca
from .models import Producto, HomeConfig, Banner
from .cart import Cart

def home(request):
    productos = Producto.objects.filter(activo=True, destacado=True).order_by("-created_at")[:8]
    home_config = HomeConfig.objects.first()
    banners = Banner.objects.filter(activo=True).order_by("orden")
    return render(request, "home.html", {
        "productos": productos,
        "cfg": home_config,
        "banners": banners
    })

def catalogo_lista(request):
    q = request.GET.get("q", "").strip()
    cat = request.GET.get("categoria", "").strip()
    mar = request.GET.get("marca", "").strip()
    minp = request.GET.get("min", "").strip()
    maxp = request.GET.get("max", "").strip()

    productos = Producto.objects.filter(activo=True)
    if q:
        productos = productos.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q))
    if cat:
        productos = productos.filter(categoria__slug=cat)
    if mar:
        productos = productos.filter(marca__slug=mar)
    if minp:
        productos = productos.filter(precio__gte=minp)
    if maxp:
        productos = productos.filter(precio__lte=maxp)

    productos = productos.order_by("-created_at")

    per_page = int(getattr(settings, "ITEMS_POR_PAGINA", 12))
    paginator = Paginator(productos, per_page)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    categorias = Categoria.objects.filter(activa=True)
    marcas = Marca.objects.filter(activa=True)

    return render(request, "catalogo/lista.html", {
        "page_obj": page_obj,
        "categorias": categorias,
        "marcas": marcas,
        "filtros": {"q": q, "categoria": cat, "marca": mar, "min": minp, "max": maxp},
    })

def producto_detalle(request, slug):
    p = get_object_or_404(Producto, slug=slug, activo=True)
    return render(request, "catalogo/detalle.html", {"p": p})

def carrito_ver(request):
    cart = Cart(request)
    raw_items = cart.items()

    ids = [i["id"] for i in raw_items]
    productos = {p.id: p for p in Producto.objects.filter(id__in=ids).prefetch_related("imagenes")}

    items = []
    total = Decimal("0.00")
    for it in raw_items:
        p = productos.get(it["id"])
        precio = Decimal(str(it["precio"]))
        cantidad = int(it["cantidad"])
        subtotal = precio * cantidad
        total += subtotal

        # 👇 tomar la primera imagen (si existe)
        img_url = None
        if p:
            primera = p.imagenes.first()
            if primera and primera.imagen:
                img_url = primera.imagen.url

        items.append({
            "id": it["id"],
            "nombre": it["nombre"],
            "precio": precio,
            "cantidad": cantidad,
            "subtotal": subtotal,
            "stock": p.stock if p else 0,
            "img_url": img_url,        
        })

    return render(request, "catalogo/carrito.html", {
        "cart_items": items,
        "total": total,
    })

def is_ajax(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"

def carrito_actualizar(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Método inválido")

    producto_id = int(request.POST.get("id"))
    cantidad = int(request.POST.get("cantidad", 1))
    p = get_object_or_404(Producto, id=producto_id, activo=True)

    # Normaliza cantidad 1..stock
    if p.stock <= 0:
        msg = "Sin stock."
        if is_ajax(request): return JsonResponse({"ok": False, "msg": msg})
        messages.error(request, msg)
        return redirect("carrito")

    if cantidad < 1:
        cantidad = 1
    if cantidad > p.stock:
        cantidad = p.stock
        messages.warning(request, f"Solo hay {p.stock} unidades disponibles. Se ajustó la cantidad.")

    cart = Cart(request)
    cart.update(p.id, cantidad)

    if is_ajax(request):
        return JsonResponse({"ok": True, "total": cart.total()})

    messages.success(request, f"Cantidad de '{p.nombre}' actualizada a {cantidad}.")
    return redirect("carrito")

def carrito_agregar(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Método inválido")

    producto_id = int(request.POST.get("id"))
    cantidad = int(request.POST.get("cantidad", 1))
    p = get_object_or_404(Producto, id=producto_id, activo=True)

    if p.stock <= 0:
        msg = "Sin stock."
        if is_ajax(request): return JsonResponse({"ok": False, "msg": msg})
        messages.error(request, msg)
        return redirect(request.META.get("HTTP_REFERER", "/carrito/"))

    cart = Cart(request)
    actual = cart.get_qty(p.id)              # cantidad ya en carrito
    disponible = p.stock - actual            # cuánto puedes agregar como máximo

    if disponible <= 0:
        msg = f"Ya alcanzaste el stock máximo disponible ({p.stock}) de '{p.nombre}'."
        if is_ajax(request): return JsonResponse({"ok": False, "msg": msg})
        messages.warning(request, msg)
        return redirect(request.META.get("HTTP_REFERER", "/carrito/"))

    if cantidad > disponible:
        cantidad = disponible
        messages.warning(request, f"Solo puedes agregar {disponible} más (stock total: {p.stock}). Cantidad ajustada.")

    cart.add(p.id, p.nombre, p.precio, cantidad)

    if is_ajax(request):
        return JsonResponse({"ok": True, "total": cart.total()})

    messages.success(request, f"Se agregó '{p.nombre}' x{cantidad} al carrito.")
    return redirect(request.META.get("HTTP_REFERER", "/carrito/"))

def carrito_eliminar(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Método inválido")
    producto_id = int(request.POST.get("id"))
    cart = Cart(request)
    cart.remove(producto_id)
    if is_ajax(request):
        return JsonResponse({"ok": True, "total": cart.total()})
    messages.success(request, "Producto eliminado del carrito.")
    return redirect("carrito")

def checkout_whatsapp(request):
    cart = Cart(request)
    items = cart.items()
    if not items:
        messages.info(request, "Tu carrito está vacío.")
        return redirect("carrito")

    # Revalidar stock antes de pasar a WhatsApp
    ids = [i["id"] for i in items]
    productos = {p.id: p for p in Producto.objects.filter(id__in=ids)}

    errores = []
    ajustes = []

    # Opcional: ¿ajustamos cantidades automáticamente al stock?
    AJUSTAR_AUTOMATICO = True

    for it in items:
        p = productos.get(it["id"])
        if not p or not p.activo or p.stock <= 0:
            errores.append(f"'{it['nombre']}' no está disponible.")
            continue
        cant = int(it["cantidad"])
        if cant > p.stock:
            if AJUSTAR_AUTOMATICO:
                # Ajustar en carrito a stock máximo
                cart.update(p.id, p.stock)
                ajustes.append(f"'{p.nombre}' ajustado a {p.stock} por stock disponible.")
            else:
                errores.append(f"'{p.nombre}' excede stock (solicitado {cant}, disponible {p.stock}).")

    # Si no ajustas automáticamente y hay errores -> bloquear
    if not AJUSTAR_AUTOMATICO and errores:
        for e in errores:
            messages.error(request, e)
        return redirect("carrito")

    # Si ajustaste automáticamente, avisa y devuelve al carrito para que el cliente vea los cambios
    if AJUSTAR_AUTOMATICO and (errores or ajustes):
        for e in errores:
            messages.error(request, e)
        for a in ajustes:
            messages.warning(request, a)
        messages.info(request, "Revisa los cambios antes de finalizar por WhatsApp.")
        return redirect("carrito")

    # Recalcular items (por si hubo ajustes) y armar mensaje
    items = cart.items()
    numero = getattr(settings, "WHATSAPP_NUMERO", "593989586619")

    lineas = ["Hola, quiero realizar este pedido:"]
    total = 0.0
    for it in items:
        subtotal = float(it["precio"]) * int(it["cantidad"])
        total += subtotal
        lineas.append(f"- {it['nombre']} x{it['cantidad']} (opcional: ${float(it['precio']):.2f} c/u)")
    lineas.append(f"Total estimado: ${total:.2f}")
    lineas.append("Nombre: <Tu nombre>")
    lineas.append("Ciudad: <Tu ciudad>")

    mensaje = quote("\n".join(lineas))
    url = f"https://wa.me/{numero}?text={mensaje}"
    return redirect(url)

def home(request):
    cfg = HomeConfig.objects.first()
    banners = Banner.objects.filter(activo=True)
    productos = []
    if not cfg or cfg.mostrar_destacados:
        cant = cfg.cantidad_destacados if cfg else 8
        productos = (Producto.objects
                     .filter(activo=True, destacado=True)
                     .order_by("-created_at")[:cant])
    return render(request, "home.html", {
        "cfg": cfg,
        "banners": banners,
        "productos": productos
    })



