"""
Catalogue API serializers.

Field names match the storefront types in frontend/src/types/catalog.ts
(snake_case, exactly as DRF serializes them). Prices are serialized as
decimal strings, e.g. "590.00", to avoid float rounding.
"""
from rest_framework import serializers

from .models import Category, Collection, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description"]


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "name", "slug"]


class CollectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "name", "slug", "description", "launch_year"]


class ProductImageSerializer(serializers.ModelSerializer):
    # Absolute URL (http://host/media/...) because the request is in the context.
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = ProductImage
        fields = ["id", "image", "alt_text", "is_primary"]


class ProductSummarySerializer(serializers.ModelSerializer):
    """Product as shown in the catalogue grid."""

    category = CategorySerializer(read_only=True)
    collection = CollectionSerializer(read_only=True)
    primary_image = serializers.SerializerMethodField()
    in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "sku",
            "name",
            "slug",
            "price",
            "category",
            "collection",
            "primary_image",
            "in_stock",
            "stock_quantity",
        ]

    def get_primary_image(self, product):
        image = product.primary_image
        if image is None:
            return None
        return ProductImageSerializer(image, context=self.context).data


class ProductDetailSerializer(ProductSummarySerializer):
    """Full product as shown on its detail page."""

    images = ProductImageSerializer(many=True, read_only=True)

    class Meta(ProductSummarySerializer.Meta):
        fields = ProductSummarySerializer.Meta.fields + ["description", "images"]
