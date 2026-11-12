from decimal import Decimal
from io import StringIO

import pytest
from django.core.management import call_command

from apps.catalog import seed_data
from apps.catalog.models import Category, Collection, Product

pytestmark = pytest.mark.django_db


def run_seed():
    out = StringIO()
    call_command("seed_catalogue", stdout=out)
    return out.getvalue()


def test_seed_data_has_the_agreed_catalogue_size():
    assert len(seed_data.CATEGORIES) == 5
    assert len(seed_data.COLLECTIONS) == 13
    assert len(seed_data.PRODUCTS) == 32


def test_seed_data_keys_are_unique():
    skus = [p["sku"] for p in seed_data.PRODUCTS]
    slugs = [p["slug"] for p in seed_data.PRODUCTS]

    assert len(set(skus)) == len(skus)
    assert len(set(slugs)) == len(slugs)


def test_seed_creates_full_catalogue():
    output = run_seed()

    assert Category.objects.count() == 5
    assert Collection.objects.count() == 13
    assert Product.objects.count() == 32
    assert Product.objects.active().count() == 32
    assert "Products: 32 created, 0 updated" in output


def test_seed_is_repeatable_without_duplicates():
    run_seed()
    output = run_seed()

    assert Category.objects.count() == 5
    assert Collection.objects.count() == 13
    assert Product.objects.count() == 32
    assert "Products: 0 created, 32 updated" in output


def test_seed_restores_seed_values_on_rerun():
    run_seed()
    Product.objects.filter(sku="MN-AH-P").update(price=Decimal("1.00"), stock_quantity=0)

    run_seed()

    product = Product.objects.get(sku="MN-AH-P")
    assert product.price == Decimal("590.00")
    assert product.stock_quantity == 8


def test_seeded_product_matches_catalogue():
    run_seed()

    product = Product.objects.with_relations().get(slug="cafe-creme-edition-gift-set")
    assert product.sku == "MN-CC-G"
    assert product.name == "Cafe Creme - Edition Gift Set"
    assert product.price == Decimal("1590.00")
    assert product.stock_quantity == 2
    assert product.category.slug == "limited-gift-sets"
    assert product.collection.slug == "cafe-creme"


def test_products_per_category():
    run_seed()

    counts = {c.slug: c.products.count() for c in Category.objects.all()}
    assert counts == {
        "fine-fragrances": 7,
        "scented-candles": 9,
        "home-fragrance": 11,
        "design-objects": 3,
        "limited-gift-sets": 2,
    }


def test_seed_editorial_texts():
    run_seed()

    collection = Collection.objects.get(slug="midnight-in-paris")
    assert collection.tagline == "Minuit, rue du Bac"
    assert collection.story.startswith("Just before midnight on the rue du Bac")

    candle = Product.objects.get(sku="MN-NP-C")
    assert candle.tagline == "A rose left by the window."
    assert candle.size == "220 g"
    assert candle.burn_time == "Approximately 50 hours"
    assert (candle.notes_top, candle.notes_heart, candle.notes_base) == (
        "Black tea leaf", "Rose petals", "Dry cedarwood",
    )
    assert candle.edition == "Édition Limitée · N° 047 / 500"

    # Fields that were not provided stay empty.
    fleur = Product.objects.get(sku="MN-FM-P")
    assert fleur.notes_heart == "Jasmine and white florals"
    assert fleur.materials == ""
    assert fleur.burn_time == ""

    after_dark = Collection.objects.get(slug="paris-after-dark")
    assert after_dark.tagline == "Le salon se vide"
    assert after_dark.image.name == "collections/paris-after-dark.jpg"

    diffuser = Product.objects.get(sku="MN-PD-D")
    assert diffuser.burn_time == "Approximately 3 months"
    assert diffuser.primary_image.image.name == "products/paris-after-dark-reed-diffuser.jpg"
    gift_set = Product.objects.get(sku="MN-PD-G")
    assert gift_set.edition == "Edition card · N° 012 / 300"
    assert gift_set.primary_image.image.name == "products/paris-after-dark-night-edition-gift-set.jpg"


def test_seed_images_are_copied_and_linked(temporary_media):
    run_seed()

    collection = Collection.objects.get(slug="midnight-in-paris")
    assert collection.image.name == "collections/midnight-in-paris.jpg"
    assert (temporary_media / "collections" / "midnight-in-paris.jpg").is_file()

    product = Product.objects.get(sku="MN-MP-P")
    image = product.primary_image
    assert image.image.name == "products/midnight-in-paris-eau-de-parfum.jpg"
    assert image.alt_text.startswith("Midnight in Paris")
    assert (temporary_media / "products" / "midnight-in-paris-eau-de-parfum.jpg").is_file()


def test_seed_images_are_not_duplicated_on_rerun():
    run_seed()
    run_seed()

    for sku, images in seed_data.PRODUCT_IMAGES.items():
        product = Product.objects.get(sku=sku)
        assert product.images.count() == len(images)
        assert product.images.filter(is_primary=True).count() == 1
