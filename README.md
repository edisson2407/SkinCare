# SkinCare
# 📋 Resumen del Proyecto

Es una tienda online con:

- Catálogo de productos (Categorías, Marcas, Productos)
- Carrito de compras basado en sesiones
- Checkout por WhatsApp (sin pasarela de pago integrada)
- Admin panel para gestionar productos, banners y configuración
- Tema visual pastel (rosa palo + verde menta)

---

# 🔑 Componentes Clave

| Archivo      | Función |
|--------------|----------|
| `models.py`  | Modelos: Producto, Categoria, Marca, ProductoImagen, HomeConfig, Banner |
| `views.py`   | Vistas: home, catálogo, detalle, carrito (agregar/actualizar/eliminar) |
| `cart.py`    | Lógica del carrito (almacenado en sesión) |
| `urls.py`    | Rutas públicas |
| `catalogo`   | Templates: lista, detalle, carrito |
| `styles.css` | Estilos responsivos (mobile-first) |

---

# 🛒 Flujo Principal

1. **Home** → muestra productos destacados + banners  
2. **Catálogo** → filtrable por categoría, marca, precio  
3. **Detalle producto** → galería de imágenes + agregar al carrito  
4. **Carrito** → actualizar cantidades, eliminar items  
5. **Checkout** → genera URL WhatsApp con el pedido  

---

# ⚙️ Variables de Configuración (.env)

```env
WHATSAPP_NUMERO=593962733227
ITEMS_POR_PAGINA=12
