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
