from django.db import models
from django.utils.text import slugify
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

class Categoria(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)
    activa = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Marca(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)
    activa = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    categoria = models.ForeignKey('Categoria', on_delete=models.PROTECT)
    marca = models.ForeignKey('Marca', on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    sku = models.CharField(max_length=40, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

# Simplificamos la ruta para Cloudinary
def producto_image_path(instance, filename):
    return f"productos/{filename}"

class ProductoImagen(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="imagenes")
    imagen = models.ImageField(upload_to=producto_image_path)
    alt_text = models.CharField(max_length=140, blank=True)
    orden = models.PositiveIntegerField(default=0)

    # ELIMINAMOS el método save complejo que causaba el error 500
    # Cloudinary se encarga de la optimización automáticamente
    
    def __str__(self):
        return f"Imagen de {self.producto.nombre}"

class HomeConfig(models.Model):
    titulo = models.CharField(max_length=120, default="Descubre el mejor SkinCare coreano")
    
    # ⬇ Ahora acepta textos largos y párrafos completos
    subtitulo = models.TextField(blank=True, default="Rutinas para cada tipo de piel")

    mostrar_destacados = models.BooleanField(default=True)
    cantidad_destacados = models.PositiveIntegerField(default=8)

    class Meta:
        verbose_name = "Configuración del Home"
        verbose_name_plural = "Configuración del Home"

    def __str__(self):
        return "Configuración del Home"

class Banner(models.Model):
    imagen = models.ImageField(upload_to="home_banners/")
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden"]

    def __str__(self):
        return f"Banner #{self.pk}"
