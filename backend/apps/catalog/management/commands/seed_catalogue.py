"""
python manage.py seed_catalogue            # safe: create what is missing, keep live edits
python manage.py seed_catalogue --reset    # disposable demo DB only: restore seed values

Seeds the MAISON NOIR catalogue (5 categories, 13 collections, 32 products)
from apps/catalog/seed_data.py.

Default (safe) mode — run it as often as you like, e.g. on every start-up:
- rows are matched by their natural keys (category/collection slug, product SKU);
  missing rows are created, so it never creates duplicates;
- an existing row is never overwritten: price, stock, active flag and any text
  an administrator changed stay as they are. Only fields that are still empty
  are filled from the seed (so new seed texts reach older databases);
- images are only added to a product that has none, and to a collection with
  no image; images uploaded or removed by an administrator are respected.
  Seed image files missing from MEDIA_ROOT are copied back, never overwritten.

--reset mode restores every seeded row to the seed values and re-links the seed
images, discarding live edits to those rows. It asks for confirmation unless
--no-input is given. Products that are not in the seed data are never touched.
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
RESET_CONFIRMATION = "reset"


class Command(BaseCommand):
    help = (
        "Seed the MAISON NOIR catalogue. Safe by default (creates missing rows, keeps live edits); "
        "--reset restores the seed values on a disposable demo database."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Restore seeded rows and images to the seed values (overwrites live edits).",
        )
        parser.add_argument(
            "--no-input",
            "--noinput",
            action="store_false",
            dest="interactive",
            help="Do not ask for confirmation before --reset.",
        )

    def handle(self, *args, reset=False, interactive=True, **options):
        if reset and interactive and not self._confirm_reset():
            self.stdout.write("Reset cancelled; nothing was changed.")
            return
        with transaction.atomic():
            self._seed(reset)

    def _confirm_reset(self):
        self.stdout.write(
            self.style.WARNING(
                "--reset overwrites price, stock, active flag, texts and images of every seeded "
                "product, category and collection. Use it only on a disposable demo database."
            )
        )
        answer = input(f"Type '{RESET_CONFIRMATION}' to continue: ")
        return answer.strip().lower() == RESET_CONFIRMATION

    def _seed(self, reset):
        sync = self._reset_rows if reset else self._create_missing_rows

        categories, cat_stats = sync(Category, "slug", seed_data.CATEGORIES)
        collections, coll_stats = sync(Collection, "slug", seed_data.COLLECTIONS)
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
        products_by_sku, prod_stats = sync(Product, "sku", products)
        linked = self._seed_images(collections, products_by_sku, reset)

        changed = "reset" if reset else "kept"
        for label, (created, existing) in (
            ("Categories", cat_stats),
            ("Collections", coll_stats),
            ("Products", prod_stats),
        ):
            self.stdout.write(f"{label}: {created} created, {existing} {changed}")
        self.stdout.write(f"Images: {linked} linked")

        self.stdout.write(
            self.style.SUCCESS(
                f"Catalogue seeded ({'reset' if reset else 'safe'} mode): {Category.objects.count()} "
                f"categories, {Collection.objects.count()} collections, {Product.objects.count()} products."
            )
        )

    # --- rows -----------------------------------------------------------------

    @staticmethod
    def _create_missing_rows(model, key, rows):
        """Create missing rows; on existing rows fill only empty fields. Returns ({key: obj}, (created, kept))."""
        objects, created_count = {}, 0
        for row in rows:
            defaults = {field: value for field, value in row.items() if field != key}
            obj, created = model.objects.get_or_create(**{key: row[key]}, defaults=defaults)
            if not created:
                empty = [f for f, v in defaults.items() if getattr(obj, f) in ("", None) and v not in ("", None)]
                for field in empty:
                    setattr(obj, field, defaults[field])
                if empty:
                    obj.save(update_fields=empty)
            objects[row[key]] = obj
            created_count += created
        return objects, (created_count, len(rows) - created_count)

    @staticmethod
    def _reset_rows(model, key, rows):
        """update_or_create each row by `key`; returns ({key: obj}, (created, reset))."""
        objects, created_count = {}, 0
        for row in rows:
            defaults = {field: value for field, value in row.items() if field != key}
            obj, created = model.objects.update_or_create(**{key: row[key]}, defaults=defaults)
            objects[row[key]] = obj
            created_count += created
        return objects, (created_count, len(rows) - created_count)

    # --- images ---------------------------------------------------------------

    def _seed_images(self, collections, products_by_sku, reset):
        """Links the seed images; returns how many collection/product images were (re)linked."""
        linked = 0

        for slug, path in seed_data.COLLECTION_IMAGES.items():
            collection = collections[slug]
            if reset or not collection.image:
                collection.image.name = self._copy_to_media(path, overwrite=reset)
                collection.save(update_fields=["image", "updated_at"])
                linked += 1
            else:
                self._copy_to_media(path, overwrite=False)  # restore a missing seed file only

        for sku, images in seed_data.PRODUCT_IMAGES.items():
            product = products_by_sku[sku]
            if not reset and product.images.exists():
                # The product already has images (seeded earlier or chosen by an admin): keep them.
                for item in images:
                    self._copy_to_media(item["file"], overwrite=False)
                continue
            for position, item in enumerate(images):
                name = self._copy_to_media(item["file"], overwrite=reset)
                is_primary = position == 0
                if is_primary:
                    # Only one primary image per product (database constraint).
                    product.images.exclude(image=name).filter(is_primary=True).update(is_primary=False)
                ProductImage.objects.update_or_create(
                    product=product,
                    image=name,
                    defaults={"alt_text": item["alt_text"], "is_primary": is_primary, "sort_order": position},
                )
                linked += 1

        return linked

    @staticmethod
    def _copy_to_media(relative_path, overwrite):
        """
        Ensures seed_images/<relative_path> exists at MEDIA_ROOT/<relative_path>; returns the stored name.
        Without `overwrite`, an existing media file is left untouched.
        """
        source = SEED_IMAGES_DIR / relative_path
        if not source.is_file():
            raise CommandError(f"Seed image not found: {source}")
        if default_storage.exists(relative_path):
            if not overwrite:
                return relative_path
            # Delete first so the storage keeps the exact name instead of adding a suffix.
            default_storage.delete(relative_path)
        with source.open("rb") as handle:
            return default_storage.save(relative_path, File(handle))
