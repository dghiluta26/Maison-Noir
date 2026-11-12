"""Root URL configuration for Maison Noir."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.core.urls")),
    path("api/", include("apps.catalog.urls")),
    path("api/auth/", include("apps.users.urls")),
]

if settings.DEBUG:
    # Serve uploaded product images during local development only.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
