"""
Admin-only catalogue API (spec A9/A10: blocked on the server for regular users).

GET /api/admin/products/            ?search=  ?is_active=true|false  ?page=
GET /api/admin/products/{slug}/

Unlike the public catalogue, administrators also see inactive products.
Read-only for P2; create/update/delete and image upload follow with the
administration panel (A9).

Access: visitor -> 401, customer -> 403, admin -> 200.
"""
from rest_framework import filters, viewsets

from apps.users.permissions import IsAdminRole

from .models import Product
from .pagination import CataloguePagination
from .serializers import AdminProductSerializer


class AdminProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AdminProductSerializer
    permission_classes = [IsAdminRole]  # uses the default JWT authentication
    pagination_class = CataloguePagination
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description", "sku", "collection__name", "category__name"]

    def get_queryset(self):
        queryset = Product.objects.with_relations()

        is_active = self.request.query_params.get("is_active")
        if self.action == "list" and is_active in ("true", "false"):
            queryset = queryset.filter(is_active=is_active == "true")

        return queryset
