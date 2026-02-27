from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("catalogo/", views.catalogo_lista, name="catalogo"),
    path("producto/<slug:slug>/", views.producto_detalle, name="producto_detalle"),
    path("carrito/", views.carrito_ver, name="carrito"),
    path("carrito/agregar/", views.carrito_agregar, name="carrito_agregar"),
    path("carrito/actualizar/", views.carrito_actualizar, name="carrito_actualizar"),
    path("carrito/eliminar/", views.carrito_eliminar, name="carrito_eliminar"),
    path("checkout/whatsapp/", views.checkout_whatsapp, name="checkout_whatsapp"),
]
