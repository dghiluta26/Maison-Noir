from django.contrib import admin

from .models import Category, Collection, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "sort_order"]
    list_editable = ["sort_order"]
    prepopulated_fields = {"slug": ["name"]}
    search_fields = ["name"]


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "launch_year", "sort_order"]
    list_editable = ["sort_order"]
    prepopulated_fields = {"slug": ["name"]}
    search_fields = ["name"]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ["image", "alt_text", "is_primary", "sort_order"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["sku", "name", "category", "collection", "price", "stock_quantity", "is_active"]
    list_filter = ["is_active", "category", "collection"]
    list_editable = ["price", "stock_quantity", "is_active"]
    search_fields = ["sku", "name", "description"]
    prepopulated_fields = {"slug": ["name"]}
    list_select_related = ["category", "collection"]
    inlines = [ProductImageInline]
