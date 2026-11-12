from rest_framework.routers import SimpleRouter

from .admin_views import AdminProductViewSet

app_name = "catalog-admin"

router = SimpleRouter()
router.register("products", AdminProductViewSet, basename="admin-product")

urlpatterns = router.urls
