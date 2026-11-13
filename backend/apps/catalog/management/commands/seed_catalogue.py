"""
python manage.py seed_catalogue

Inserts the MAISON NOIR catalogue (5 categories, 13 collections, 32 products)
from apps/catalog/seed_data.py.

The command is repeatable: rows are matched by their natural keys
(category/collection slug, product SKU) and updated in place, so running it
again never creates duplicates. Seed values overwrite edits made to the same
rows (e.g. price or stock changed in the admin). Products that are not in the
seed data are left untouched.

Images: the files in apps/catalog/seed_images/ are copied to MEDIA_ROOT (same
relative path, overwritten on every run) and linked to their collection or
product. A seeded product image is matched by its file path, so re-running the
seed never duplicates it; it becomes the product's primary image.
"""
from decimal import Decimal
from pathlib import Path

from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.catalog import seed_data
from apps.catalog.models import Category, Collection, Product, ProductImage

SEED_IMAGES_DIR = Path(seed_data.__file__).resolve().parent / "seed_images"


class Command(BaseCommand):
    help = "Insert or update the MAISON NOIR catalogue seed data (safe to run repeatedly)."

    @transaction.atomic
    def handle(self, *args, **options):
        categories, cat_stats = self._upsert(Category, "slug", seed_data.CATEGORIES)
        collections, coll_stats = self._upsert(Collection, "slug", seed_data.COLLECTIONS)

        products = [
            {
                **item,
                "category": categories[item["category"]],
                "collection": collections[item["collection"]],
                "price": Decimal(item["price"]),
                "is_active": True,
            }
            for item in seed_data.PRODUCTS
        ]
        products_by_sku, prod_stats = self._upsert(Product, "sku", products)
        image_count = self._seed_images(collections, products_by_sku)

        for label, (created, updated) in (
            ("Categories", cat_stats),
            ("Collections", coll_stats),
            ("Products", prod_stats),
        ):
            self.stdout.write(f"{label}: {created} created, {updated} updated")
        self.stdout.write(f"Images: {image_count} copied to media")

        self.stdout.write(
            self.style.SUCCESS(
                f"Catalogue seeded: {Category.objects.count()} categories, "
                f"{Collection.objects.count()} collections, {Product.objects.count()} products."
            )
        )

    def _seed_images(self, collections, products_by_sku):
        """Copies the seed images to media and links them; returns how many were copied."""
        for slug, path in seed_data.COLLECTION_IMAGES.items():
            collection = collections[slug]
            collection.image.name = self._copy_to_media(path)
            collection.save(update_fields=["image", "updated_at"])

        for sku, images in seed_data.PRODUCT_IMAGES.items():
            product = products_by_sku[sku]
            for position, item in enumerate(images):
                name = self._copy_to_media(item["file"])
                is_primary = position == 0
                if is_primary:
                    # Only one primary image per product (database constraint).
                    product.images.exclude(image=name).filter(is_primary=True).update(is_primary=False)
                ProductImage.objects.update_or_create(
                    product=product,
                    image=name,
                    defaults={"alt_text": item["alt_text"], "is_primary": is_primary, "sort_order": position},
                )

        return len(seed_data.COLLECTION_IMAGES) + sum(len(i) for i in seed_data.PRODUCT_IMAGES.values())

    @staticmethod
    def _copy_to_media(relative_path):
        """Copies seed_images/<relative_path> to MEDIA_ROOT/<relative_path>; returns the stored name."""
        source = SEED_IMAGES_DIR / relative_path
        if not source.is_file():
            raise CommandError(f"Seed image not found: {source}")
        # Delete first so the storage keeps the exact name instead of adding a suffix.
        if default_storage.exists(relative_path):
            default_storage.delete(relative_path)
        with source.open("rb") as handle:
            return default_storage.save(relative_path, File(handle))

    @staticmethod
    def _upsert(model, key, rows):
        """update_or_create each row by `key`; returns ({key: obj}, (created, updated))."""
        objects, created_count = {}, 0
        for row in rows:
            defaults = {field: value for field, value in row.items() if field != key}
            obj, created = model.objects.update_or_create(**{key: row[key]}, defaults=defaults)
            objects[row[key]] = obj
            created_count += created
        return objects, (created_count, len(rows) - created_count)
