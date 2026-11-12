"""
Public, read-only catalogue API.

GET /api/categories/
GET /api/collections/
GET /api/products/                 ?search=  ?category=<slug>  ?collection=<slug>  ?page=
GET /api/products/{slug}/

Only active products are visible; an inactive or unknown slug returns 404.
The catalogue is public and ignores any Authorization header.
"""
from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny

from .models import Category, Collection, Product
from .pagination import CataloguePagination
from .serializers import (
    CategoryListSerializer,
    CollectionListSerializer,
    ProductDetailSerializer,
    ProductSummarySerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    permission_classes = [AllowAny]
    authentication_classes = []  # public: ignore (possibly expired) tokens
    pagination_class = None
    lookup_field = "slug"


class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionListSerializer
    permission_classes = [AllowAny]
    authentication_classes = []  # public: ignore (possibly expired) tokens
    pagination_class = None
    lookup_field = "slug"


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    authentication_classes = []  # public: ignore (possibly expired) tokens
    pagination_class = CataloguePagination
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description", "sku", "collection__name", "category__name"]

    def get_queryset(self):
        queryset = Product.objects.active().with_relations()

        if self.action == "list":
            category = self.request.query_params.get("category")
            collection = self.request.query_params.get("collection")
            if category:
                queryset = queryset.filter(category__slug=category)
            if collection:
                queryset = queryset.filter(collection__slug=collection)

        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductSummarySerializer
