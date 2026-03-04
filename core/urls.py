from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("panel/", admin.site.urls),
    path("", include("catalogo.urls")),   # <- rutas públicas
    
    # 1. Agregamos la ruta de recarga automática de Tailwind
    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)