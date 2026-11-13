from io import StringIO

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from rest_framework.test import APIClient

from apps.catalog.models import Product, ProductImage

pytestmark = pytest.mark.django_db

TINY_GIF = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00"
    b"\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
)

SUMMARY_FIELDS = {
    "id", "sku", "name", "slug", "price", "category", "collection",
    "primary_image", "in_stock", "stock_quantity",
}
# Optional product-page details, returned by the detail endpoint only.
DETAIL_TEXT_FIELDS = {
    "tagline", "size", "burn_time", "includes", "notes_top", "notes_heart", "notes_base",
    "materials", "edition", "ritual",
}


@pytest.fixture(autouse=True)
def catalogue(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    call_command("seed_catalogue", stdout=StringIO())


@pytest.fixture
def api():
    return APIClient()


# --- Products: list ------------------------------------------------------


def test_product_list_returns_paginated_catalogue(api):
    response = api.get("/api/products/")

    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"count", "next", "previous", "results"}
    assert body["count"] == 32
    assert len(body["results"]) == 32
    assert body["next"] is None


def test_product_list_item_shape(api):
    item = api.get("/api/products/").json()["results"][0]

    assert set(item) == SUMMARY_FIELDS
    assert item["sku"] == "MN-AH-P"
    assert item["slug"] == "after-hours-eau-de-parfum"
    assert item["price"] == "590.00"
    assert item["category"] == {"id": item["category"]["id"], "name": "Fine Fragrances", "slug": "fine-fragrances"}
    assert item["collection"]["slug"] == "after-hours"
    assert item["primary_image"] is None
    assert item["in_stock"] is True
    assert item["stock_quantity"] == 8


def test_product_list_is_public_without_login(api):
    assert api.get("/api/products/").status_code == 200


def test_inactive_products_are_hidden(api):
    Product.objects.filter(sku="MN-AH-P").update(is_active=False)

    body = api.get("/api/products/").json()

    assert body["count"] == 31
    assert "MN-AH-P" not in {p["sku"] for p in body["results"]}


def test_page_size_can_be_reduced(api):
    body = api.get("/api/products/?page_size=10").json()

    assert body["count"] == 32
    assert len(body["results"]) == 10
    assert body["next"] is not None


def test_search_by_name(api):
    # Every search term must match (name, description, SKU, collection or category).
    body = api.get("/api/products/?search=golden hour").json()

    assert body["count"] == 4
    assert all("Golden Hour" in p["name"] for p in body["results"])


def test_search_by_sku_and_description(api):
    assert api.get("/api/products/?search=MN-CC-G").json()["count"] == 1
    assert api.get("/api/products/?search=labdanum").json()["count"] == 3


def test_search_without_matches_returns_empty_list(api):
    body = api.get("/api/products/?search=nothing-like-this").json()

    assert body["count"] == 0
    assert body["results"] == []


def test_filter_by_category(api):
    body = api.get("/api/products/?category=limited-gift-sets").json()

    assert body["count"] == 2
    assert {p["category"]["slug"] for p in body["results"]} == {"limited-gift-sets"}


def test_filter_by_collection(api):
    body = api.get("/api/products/?collection=cafe-creme").json()

    assert body["count"] == 5


def test_product_list_uses_constant_number_of_queries(api, django_assert_max_num_queries):
    # count + products/category/collection + images, independent of the 32 rows
    with django_assert_max_num_queries(3):
        api.get("/api/products/")


# --- Products: detail ----------------------------------------------------


def test_product_detail_by_slug(api):
    response = api.get("/api/products/cafe-creme-edition-gift-set/")

    assert response.status_code == 200
    body = response.json()
    assert set(body) == SUMMARY_FIELDS | DETAIL_TEXT_FIELDS | {"description", "images"}
    assert body["sku"] == "MN-CC-G"
    assert body["price"] == "1590.00"
    assert body["description"].startswith("An espresso linen case opens")
    assert body["includes"].endswith("Le Plateau Café")
    assert len(body["images"]) == 1
    assert body["images"][0]["is_primary"] is True
    assert body["images"][0]["image"].endswith("/media/products/cafe-creme-edition-gift-set.jpg")


def test_unknown_slug_returns_404(api):
    assert api.get("/api/products/does-not-exist/").status_code == 404


def test_inactive_product_detail_returns_404(api):
    Product.objects.filter(slug="after-hours-eau-de-parfum").update(is_active=False)

    assert api.get("/api/products/after-hours-eau-de-parfum/").status_code == 404


def test_images_are_returned_as_absolute_urls(api):
    product = Product.objects.get(sku="MN-AH-P")
    ProductImage.objects.create(
        product=product,
        image=SimpleUploadedFile("bottle.gif", TINY_GIF, "image/gif"),
        alt_text="After Hours bottle",
        is_primary=True,
    )

    body = api.get("/api/products/after-hours-eau-de-parfum/").json()

    assert body["primary_image"]["image"].startswith("http://testserver/media/products/")
    assert body["primary_image"]["alt_text"] == "After Hours bottle"
    assert body["images"][0]["is_primary"] is True


def test_catalogue_is_read_only(api):
    assert api.post("/api/products/", {}).status_code in (401, 403, 405)
    assert api.delete("/api/products/after-hours-eau-de-parfum/").status_code in (401, 403, 405)


# --- Categories and collections ------------------------------------------


def test_category_list(api):
    response = api.get("/api/categories/")

    assert response.status_code == 200
    body = response.json()
    assert [c["slug"] for c in body] == [
        "fine-fragrances",
        "scented-candles",
        "home-fragrance",
        "design-objects",
        "limited-gift-sets",
    ]
    assert set(body[0]) == {"id", "name", "slug", "description"}


def test_collection_list(api):
    body = api.get("/api/collections/").json()

    assert len(body) == 13
    assert body[0]["slug"] == "after-hours"
    assert set(body[0]) == {"id", "name", "slug", "description", "tagline", "story", "image", "launch_year"}
