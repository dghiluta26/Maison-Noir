from decimal import Decimal

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.db.models import ProtectedError

from apps.catalog.models import Category, Collection, Product, ProductImage

pytestmark = pytest.mark.django_db

# Smallest valid GIF, so ImageField accepts the upload without real files.
TINY_GIF = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00"
    b"\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
)


@pytest.fixture(autouse=True)
def media_in_tmp(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path


@pytest.fixture
def category():
    return Category.objects.create(name="Fine Fragrances")


@pytest.fixture
def collection():
    return Collection.objects.create(name="After Hours", launch_year=2026)


def make_product(category, collection, **overrides):
    data = {
        "sku": "MN-AH-P",
        "name": "After Hours - Eau de Parfum",
        "category": category,
        "collection": collection,
        "price": Decimal("590.00"),
        "stock_quantity": 8,
    }
    data.update(overrides)
    return Product.objects.create(**data)


def make_image(product, **overrides):
    data = {"product": product, "image": SimpleUploadedFile("img.gif", TINY_GIF, "image/gif")}
    data.update(overrides)
    return ProductImage.objects.create(**data)


def test_slugs_are_generated_from_names(category, collection):
    product = make_product(category, collection)

    assert category.slug == "fine-fragrances"
    assert collection.slug == "after-hours"
    assert product.slug == "after-hours-eau-de-parfum"


def test_explicit_slug_is_kept(category, collection):
    product = make_product(category, collection, slug="custom-slug")

    assert product.slug == "custom-slug"


def test_product_slug_must_be_unique(category, collection):
    make_product(category, collection)

    with pytest.raises(IntegrityError):
        make_product(category, collection, sku="MN-AH-X")


def test_product_sku_must_be_unique(category, collection):
    make_product(category, collection)

    with pytest.raises(IntegrityError):
        make_product(category, collection, name="Another name")


def test_database_rejects_negative_price(category, collection):
    with pytest.raises(IntegrityError):
        make_product(category, collection, price=Decimal("-1.00"))


def test_database_rejects_negative_stock(category, collection):
    product = make_product(category, collection)

    with pytest.raises(IntegrityError):
        Product.objects.filter(pk=product.pk).update(stock_quantity=-1)


def test_database_rejects_launch_year_out_of_range():
    with pytest.raises(IntegrityError):
        Collection.objects.create(name="Too Old", launch_year=1850)


def test_in_stock_reflects_stock_quantity(category, collection):
    product = make_product(category, collection, stock_quantity=0)
    assert product.in_stock is False

    product.stock_quantity = 2
    assert product.in_stock is True


def test_active_queryset_hides_inactive_products(category, collection):
    visible = make_product(category, collection)
    make_product(category, collection, sku="MN-OLD", name="Retired", is_active=False)

    assert list(Product.objects.active()) == [visible]


def test_category_with_products_cannot_be_deleted(category, collection):
    make_product(category, collection)

    with pytest.raises(ProtectedError):
        category.delete()


def test_collection_with_products_cannot_be_deleted(category, collection):
    make_product(category, collection)

    with pytest.raises(ProtectedError):
        collection.delete()


def test_deleting_product_deletes_its_images(category, collection):
    product = make_product(category, collection)
    make_image(product)

    product.delete()

    assert ProductImage.objects.count() == 0


def test_only_one_primary_image_per_product(category, collection):
    product = make_product(category, collection)
    make_image(product, is_primary=True)

    with pytest.raises(IntegrityError):
        make_image(product, is_primary=True)


def test_primary_image_prefers_flagged_image_then_first(category, collection):
    product = make_product(category, collection)
    assert product.primary_image is None

    first = make_image(product, sort_order=0)
    assert product.primary_image == first

    flagged = make_image(product, sort_order=1, is_primary=True)
    assert product.primary_image == flagged


def test_with_relations_avoids_extra_queries(category, collection, django_assert_num_queries):
    for i in range(3):
        make_image(make_product(category, collection, sku=f"MN-{i}", name=f"Product {i}"))

    # 1 query for products + category + collection, 1 for all images.
    with django_assert_num_queries(2):
        for product in Product.objects.with_relations():
            _ = product.category.name, product.collection.name, product.primary_image
