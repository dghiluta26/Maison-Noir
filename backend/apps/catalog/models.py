"""
Catalogue models.

Based on the MAISON NOIR E-R model:
- COLLECTIONS  -> Collection (collection_name, description, launch_year)
- PRODUCTS     -> Product (product_name, product_type, price, stock_quantity,
                  scent_description); `product_type` is represented by Category.
Extended for the storefront with Category, ProductImage, SKU, slugs and an
active flag (agreed in task 0.1 / P2 plan section 5).

Business rules enforced in the database:
- price and stock can never be negative;
- product slug and SKU are unique;
- a product has at most one primary image;
- categories/collections that still have products cannot be deleted.
"""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SlugFromNameMixin(models.Model):
    """Fills `slug` from `name` when it is left empty."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(SlugFromNameMixin, TimeStampedModel):
    """Product type, e.g. Fine Fragrances, Scented Candles (5 in P2)."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    sort_order = models.PositiveSmallIntegerField(
        default=0, help_text="Lower numbers are shown first."
    )

    class Meta:
        db_table = "categories"
        verbose_name_plural = "categories"
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class Collection(SlugFromNameMixin, TimeStampedModel):
    """Scent universe that groups products, e.g. After Hours (COLLECTIONS)."""

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=170, unique=True)
    description = models.TextField(blank=True, help_text="Short summary (one sentence).")
    tagline = models.CharField(
        max_length=200, blank=True, help_text='Collection page subtitle, e.g. "Minuit, rue du Bac".'
    )
    story = models.TextField(blank=True, help_text="Long text shown on the collection page.")
    image = models.ImageField(
        upload_to="collections/", blank=True, help_text="Hero picture of the collection page."
    )
    launch_year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(2000), MaxValueValidator(2100)],
    )
    sort_order = models.PositiveSmallIntegerField(
        default=0, help_text="Lower numbers are shown first."
    )

    class Meta:
        db_table = "collections"
        ordering = ["sort_order", "name"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(launch_year__isnull=True)
                | models.Q(launch_year__gte=2000, launch_year__lte=2100),
                name="collection_launch_year_range",
            ),
        ]

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def active(self):
        """Products visible to the public storefront."""
        return self.filter(is_active=True)

    def in_stock(self):
        return self.filter(stock_quantity__gt=0)

    def with_relations(self):
        """Load category, collection and images without N+1 queries."""
        return self.select_related("category", "collection").prefetch_related("images")


class Product(SlugFromNameMixin, TimeStampedModel):
    """A sellable item (PRODUCTS)."""

    sku = models.CharField("SKU", max_length=20, unique=True, help_text='e.g. "MN-AH-P"')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField(blank=True, help_text="Scent / design description.")
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name="products"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Price in lei (RON).",
    )
    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(
        default=True, help_text="Inactive products are hidden from the storefront."
    )

    # Optional product-page details (empty values are simply not shown).
    tagline = models.CharField(
        max_length=200, blank=True, help_text='One line under the name, e.g. "The last cup of black tea."'
    )
    size = models.CharField(max_length=50, blank=True, help_text='e.g. "100 ml" or "220 g".')
    burn_time = models.CharField(
        max_length=100,
        blank=True,
        help_text='How long it lasts: candle burn time ("Approximately 50 hours") '
        'or diffuser duration ("Approximately 3 months").',
    )
    notes_top = models.CharField("top notes", max_length=200, blank=True)
    notes_heart = models.CharField("heart notes", max_length=200, blank=True)
    notes_base = models.CharField("base notes", max_length=200, blank=True)
    materials = models.TextField(blank=True)
    edition = models.CharField(
        max_length=100, blank=True, help_text='e.g. "Édition Limitée · N° 047 / 500".'
    )
    ritual = models.TextField(blank=True, help_text="How to use or enjoy the product.")

    objects = ProductQuerySet.as_manager()

    class Meta:
        db_table = "products"
        # Catalogue order = insertion order of the seed (grouped by collection).
        ordering = ["id"]
        indexes = [
            models.Index(fields=["is_active", "category"], name="product_active_category_idx"),
            models.Index(fields=["is_active", "collection"], name="product_active_coll_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=0), name="product_price_non_negative"
            ),
            # stock_quantity >= 0 is enforced by PositiveIntegerField's own CHECK.
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def in_stock(self) -> bool:
        return self.stock_quantity > 0

    @property
    def primary_image(self):
        """The primary image, else the first image, else None (uses prefetched images)."""
        images = list(self.images.all())
        return next((img for img in images if img.is_primary), images[0] if images else None)


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "product_images"
        ordering = ["sort_order", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                condition=models.Q(is_primary=True),
                name="product_single_primary_image",
            ),
        ]

    def __str__(self):
        return f"Image {self.pk} of {self.product.sku}"
