"""
python manage.py seed_catalogue

Inserts the MAISON NOIR catalogue (5 categories, 13 collections, 32 products)
from apps/catalog/seed_data.py.

The command is repeatable: rows are matched by their natural keys
(category/collection slug, product SKU) and updated in place, so running it
again never creates duplicates. Seed values overwrite edits made to the same
rows (e.g. price or stock changed in the admin). Products that are not in the
seed data are left untouched.
"""
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.catalog import seed_data
from apps.catalog.models import Category, Collection, Product


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
        _, prod_stats = self._upsert(Product, "sku", products)

        for label, (created, updated) in (
            ("Categories", cat_stats),
            ("Collections", coll_stats),
            ("Products", prod_stats),
        ):
            self.stdout.write(f"{label}: {created} created, {updated} updated")

        self.stdout.write(
            self.style.SUCCESS(
                f"Catalogue seeded: {Category.objects.count()} categories, "
                f"{Collection.objects.count()} collections, {Product.objects.count()} products."
            )
        )

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
