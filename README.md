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
```
# 📋 Requisitos Previos

- **Python:** 3.10 o superior (recomendado 3.11+)
  
# 📦 Instalación de Dependencias

Para instalar todas las dependencias del proyecto, ejecuta el siguiente comando en la raíz del proyecto:

```bash
pip install -r requirements.txt
```

# 🚀 Levantar un Proyecto en Django (Guía Esencial)

## 1️⃣ Aplicar Migraciones

Antes de iniciar el servidor, ejecuta:

```bash
python manage.py migrate
```

---

## 2️⃣ Crear Superusuario (Admin)

Para crear un usuario administrador:

```bash
python manage.py createsuperuser
```

Luego podrás acceder al panel en:

```
http://127.0.0.1:8000/admin/
```

---

## 3️⃣ Levantar el Servidor en Local

Para iniciar el proyecto en entorno local:

```bash
python manage.py runserver
```

El proyecto estará disponible en:

```
http://127.0.0.1:8000/
```

Si deseas usar otro puerto:

```bash
python manage.py runserver 8001
```

---

## ✅ Flujo rápido recomendado

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
