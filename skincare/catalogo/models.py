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
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True, blank=True)
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

def producto_image_path(instance, filename):
    return f"productos/{instance.producto_id}/{filename}"

class ProductoImagen(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="imagenes")
    imagen = models.ImageField(upload_to=producto_image_path)
    alt_text = models.CharField(max_length=140, blank=True)
    orden = models.PositiveIntegerField(default=0)

    MAX_SIZE = (1080, 1080)
    MAX_BYTES = 300 * 1024  # 300 KB

    def save(self, *args, **kwargs):
        # Guardado normal primero
        super().save(*args, **kwargs)

        # Re-abrir y procesar
        img = Image.open(self.imagen.path).convert("RGB")
        # Redimensionar manteniendo proporción y encajar en 1080x1080 (cover centrado)
        img.thumbnail(self.MAX_SIZE, Image.Resampling.LANCZOS)
        # Si no queda cuadrada, pegamos sobre lienzo 1080x1080 (fondo blanco)
        if img.size != self.MAX_SIZE:
            canvas = Image.new("RGB", self.MAX_SIZE, (255, 255, 255))
            x = (self.MAX_SIZE[0] - img.size[0]) // 2
            y = (self.MAX_SIZE[1] - img.size[1]) // 2
            canvas.paste(img, (x, y))
            img = canvas

        # Comprimir hasta <= 300 KB
        quality = 90
        while quality > 40:
            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=quality, optimize=True)
            size = buffer.tell()
            if size <= self.MAX_BYTES:
                break
            quality -= 5

        # Reemplazar archivo
        file_content = ContentFile(buffer.getvalue())
        filename = self.imagen.name.rsplit("/", 1)[-1]
        self.imagen.save(filename, file_content, save=False)
        super().save(update_fields=["imagen"])

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
    titulo = models.CharField(max_length=120, blank=True)
    texto = models.CharField(max_length=220, blank=True)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden"]

    def __str__(self):
        return self.titulo or f"Banner #{self.pk}"
