from decimal import Decimal
from io import StringIO

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command

from apps.catalog import seed_data
from apps.catalog.models import Category, Collection, Product, ProductImage

# Smallest valid GIF, so ImageField accepts the upload without real files.
TINY_GIF = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00"
    b"\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
)

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
    assert "Products: 32 created, 0 kept" in output


def test_seed_is_repeatable_without_duplicates():
    run_seed()
    output = run_seed()

    assert Category.objects.count() == 5
    assert Collection.objects.count() == 13
    assert Product.objects.count() == 32
    assert "Products: 0 created, 32 kept" in output


def test_safe_seed_keeps_live_edits():
    """Normal start-up seeding must never overwrite what an administrator changed."""
    run_seed()
    Product.objects.filter(sku="MN-AH-P").update(
        price=Decimal("1.00"), stock_quantity=0, is_active=False, name="Renamed by admin"
    )
    Category.objects.filter(slug="fine-fragrances").update(description="Edited by admin")

    run_seed()

    product = Product.objects.get(sku="MN-AH-P")
    assert product.price == Decimal("1.00")
    assert product.stock_quantity == 0
    assert product.is_active is False
    assert product.name == "Renamed by admin"
    assert Category.objects.get(slug="fine-fragrances").description == "Edited by admin"


def test_safe_seed_fills_only_empty_fields():
    run_seed()
    Product.objects.filter(sku="MN-NP-C").update(tagline="", size="")

    run_seed()

    candle = Product.objects.get(sku="MN-NP-C")
    assert candle.tagline == "A rose left by the window."
    assert candle.size == "220 g"


def test_safe_seed_keeps_admin_chosen_images():
    run_seed()
    product = Product.objects.get(sku="MN-AH-P")
    product.images.all().delete()
    admin_image = ProductImage.objects.create(
        product=product,
        image=SimpleUploadedFile("admin-photo.gif", TINY_GIF, "image/gif"),
        is_primary=True,
    )

    run_seed()

    assert list(product.images.all()) == [admin_image]


def test_safe_seed_restores_missing_seed_files(temporary_media):
    run_seed()
    seed_file = temporary_media / "products" / "after-hours-eau-de-parfum.jpg"
    seed_file.unlink()

    run_seed()

    assert seed_file.is_file()


def test_reset_restores_seed_values():
    run_seed()
    Product.objects.filter(sku="MN-AH-P").update(price=Decimal("1.00"), stock_quantity=0, is_active=False)

    out = StringIO()
    call_command("seed_catalogue", reset=True, interactive=False, stdout=out)

    product = Product.objects.get(sku="MN-AH-P")
    assert product.price == Decimal("590.00")
    assert product.stock_quantity == 8
    assert product.is_active is True
    assert "Products: 0 created, 32 reset" in out.getvalue()


def test_reset_asks_for_confirmation_and_can_be_cancelled(monkeypatch):
    run_seed()
    Product.objects.filter(sku="MN-AH-P").update(price=Decimal("1.00"))
    monkeypatch.setattr("builtins.input", lambda prompt: "no")

    out = StringIO()
    call_command("seed_catalogue", reset=True, stdout=out)

    assert "Reset cancelled" in out.getvalue()
    assert Product.objects.get(sku="MN-AH-P").price == Decimal("1.00")


def test_reset_runs_after_typing_reset(monkeypatch):
    run_seed()
    Product.objects.filter(sku="MN-AH-P").update(price=Decimal("1.00"))
    monkeypatch.setattr("builtins.input", lambda prompt: "reset")

    call_command("seed_catalogue", reset=True, stdout=StringIO())

    assert Product.objects.get(sku="MN-AH-P").price == Decimal("590.00")


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

    assert Collection.objects.get(slug="maison-blanche").tagline == "Le calme du matin"
    duo = Product.objects.get(sku="MN-MB-H")
    assert duo.includes.endswith("Calacatta marble tray")
    assert duo.primary_image.image.name == "products/maison-blanche-home-ritual-duo.jpg"

    soft_linen = Collection.objects.get(slug="soft-linen")
    assert soft_linen.tagline == "Le pli du lin"
    assert soft_linen.image.name == "collections/soft-linen.jpg"
    for sku in ("MN-SL-P", "MN-SL-C", "MN-SL-D"):
        product = Product.objects.get(sku=sku)
        assert (product.notes_top, product.notes_heart, product.notes_base) == (
            "Pear", "Cotton blossom", "White musk",
        )
        assert product.primary_image is not None

    ambre = Collection.objects.get(slug="ambre-parisien")
    assert ambre.tagline == "Le bois des loges"
    assert ambre.image.name == "collections/ambre-parisien.jpg"
    for sku in ("MN-AP-P", "MN-AP-C", "MN-AP-D"):
        product = Product.objects.get(sku=sku)
        assert (product.notes_top, product.notes_heart, product.notes_base) == (
            "Amber accord", "Labdanum", "Sandalwood",
        )
        assert product.primary_image is not None

    appartement = Collection.objects.get(slug="l-appartement")
    assert appartement.tagline == "Les fenêtres ouvertes"
    assert appartement.image.name == "collections/l-appartement.jpg"
    for sku in ("MN-LA-C", "MN-LA-D"):
        product = Product.objects.get(sku=sku)
        assert (product.notes_top, product.notes_heart, product.notes_base) == (
            "Fig leaf", "Cedar", "Polished wood",
        )
        assert product.primary_image is not None

    chambre = Collection.objects.get(slug="chambre-noire")
    assert chambre.tagline == "Derrière le rideau rouge"
    assert chambre.image.name == "collections/chambre-noire.jpg"
    for sku in ("MN-CN-C", "MN-CN-D"):
        product = Product.objects.get(sku=sku)
        assert (product.notes_top, product.notes_heart, product.notes_base) == (
            "Dry cedar", "Incense", "Soft leather",
        )
        assert product.primary_image is not None

    assert Collection.objects.get(slug="fleur-de-maison").tagline == "Les pivoines du dimanche"
    fleur_duo = Product.objects.get(sku="MN-FM-H")
    assert fleur_duo.notes_heart == "Peony"
    assert fleur_duo.includes.endswith("Matching marble tray")
    assert fleur_duo.primary_image.image.name == "products/fleur-de-maison-home-ritual-duo.jpg"

    assert Collection.objects.get(slug="santal-residence").tagline == "Dans l’atelier d’ébénisterie"
    santal_duo = Product.objects.get(sku="MN-SR-H")
    assert (santal_duo.notes_top, santal_duo.notes_heart, santal_duo.notes_base) == (
        "Cedar", "Sandalwood", "Dry amber",
    )
    assert santal_duo.includes.endswith("Emperador marble tray")
    assert santal_duo.primary_image.image.name == "products/santal-residence-home-ritual-duo.jpg"

    cafe = Collection.objects.get(slug="cafe-creme")
    assert cafe.tagline == "Un matin au comptoir"
    assert cafe.image.name == "collections/cafe-creme.jpg"
    for sku in ("MN-CC-P", "MN-CC-C", "MN-CC-D", "MN-CC-G"):
        product = Product.objects.get(sku=sku)
        assert (product.notes_top, product.notes_heart, product.notes_base) == (
            "Roasted coffee", "Vanilla", "Tonka bean",
        )
        assert product.primary_image is not None
    tray = Product.objects.get(sku="MN-CC-O")
    assert tray.materials.startswith("Glazed espresso ceramic")
    assert tray.notes_top == ""  # unscented object
    assert tray.primary_image.image.name == "products/cafe-creme-le-plateau-cafe.jpg"

    after_hours = Collection.objects.get(slug="after-hours")
    assert after_hours.tagline == "Quand le salon s’apaise"
    assert after_hours.image.name == "collections/after-hours.jpg"
    for sku in ("MN-AH-P", "MN-AH-C", "MN-AH-D"):
        product = Product.objects.get(sku=sku)
        assert (product.notes_top, product.notes_heart, product.notes_base) == (
            "Bergamot", "Iris", "Musk",
        )
        assert product.primary_image is not None
    nocturne = Product.objects.get(sku="MN-AH-O")
    assert nocturne.materials.startswith("Honed dark smoked stone")
    assert nocturne.primary_image.image.name == "products/after-hours-nocturne-tray.jpg"


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


def test_every_seeded_product_has_a_primary_image():
    """Project spec 2.1: every product has an image, loaded through the seed script."""
    assert set(seed_data.PRODUCT_IMAGES) == {p["sku"] for p in seed_data.PRODUCTS}
    run_seed()

    without_image = [p.sku for p in Product.objects.all() if p.primary_image is None]
    assert without_image == []

    golden = Collection.objects.get(slug="golden-hour")
    assert golden.tagline == "La lumière sur la Seine"
    assert golden.image.name == "collections/golden-hour.jpg"
    assert Product.objects.get(sku="MN-GH-O").materials.startswith("Polished calcite onyx")


def test_seed_images_are_not_duplicated_on_rerun():
    run_seed()
    run_seed()

    for sku, images in seed_data.PRODUCT_IMAGES.items():
        product = Product.objects.get(sku=sku)
        assert product.images.count() == len(images)
        assert product.images.filter(is_primary=True).count() == 1
