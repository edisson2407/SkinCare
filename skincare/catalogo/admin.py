from django.contrib import admin
from .models import Categoria, Marca, Producto, ProductoImagen
from .models import HomeConfig, Banner


class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 1


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("nombre",)}
    list_display = ("nombre", "categoria", "marca", "precio", "stock", "activo", "destacado")
    list_filter = ("categoria", "marca", "activo", "destacado")
    search_fields = ("nombre", "descripcion", "sku")
    inlines = [ProductoImagenInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Filtra por el campo correcto de Producto: 'activo'
        return qs.filter(activo=True)
        # Si prefieres ver TODOS en el admin, usa:
        # return qs


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("nombre",)}
    # Deja 'activa' si tu modelo Categoria tiene ese booleano.
    # Si en tu modelo es 'activo', cambia a ("nombre", "activo")
    list_display = ("nombre", "activa")


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("nombre",)}
    # Igual que arriba: usa 'activa' solo si el modelo Marca lo define así.
    list_display = ("nombre", "activa")


@admin.register(HomeConfig)
class HomeConfigAdmin(admin.ModelAdmin):
    # Opcional: muestra algo en la lista
    list_display = ("titulo", "mostrar_destacados", "cantidad_destacados")

    def has_add_permission(self, request):
        # Limita a un solo registro de configuración
        return not HomeConfig.objects.exists()


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("titulo", "orden", "activo")
    list_editable = ("orden", "activo")
