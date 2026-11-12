# Catalogue API

Base URL (local): `http://localhost:8000/api`

All catalogue endpoints are **public** (no login) and **read-only** (`GET` only).
Responses are JSON with `snake_case` field names, matching
`frontend/src/types/catalog.ts`.

| Method | Endpoint | Returns |
|---|---|---|
| GET | `/api/products/` | Paginated list of active products (`ProductSummary`) |
| GET | `/api/products/{slug}/` | One active product (`ProductDetail`) |
| GET | `/api/categories/` | All categories (not paginated) |
| GET | `/api/collections/` | All collections (not paginated) |

## Conventions

- **Prices** are decimal **strings** in lei, e.g. `"590.00"` (avoids float rounding). Format them for display; do not do arithmetic on floats.
- **Inactive products** (`is_active = false` in the admin) never appear in the list, and their detail URL returns `404`.
- **Images**: `image` is an absolute URL (`http://localhost:8000/media/products/...`). Products without images have `primary_image: null` and `images: []`; the UI must show a placeholder.
- `primary_image` is the image marked primary, otherwise the first image, otherwise `null`.
- **Order**: products are returned in catalogue order (grouped by collection), categories and collections in their display order.
- **CORS**: browser requests are accepted from the origins in `CORS_ALLOWED_ORIGINS` (`.env`), by default `http://localhost:5173`.

---

## GET `/api/products/`

### Query parameters

| Parameter | Example | Description |
|---|---|---|
| `search` | `?search=golden hour` | Case-insensitive text search in name, description, SKU, collection name and category name. With several words, **every** word must match. |
| `category` | `?category=limited-gift-sets` | Only products in this category (category slug). |
| `collection` | `?collection=cafe-creme` | Only products in this collection (collection slug). |
| `page` | `?page=2` | Page number (starts at 1). |
| `page_size` | `?page_size=12` | Products per page. Default **48** (the whole P2 catalogue fits on page 1), maximum 100. |

Parameters can be combined, e.g. `?category=scented-candles&search=amber`.
An unknown `category`/`collection` slug or a search without matches returns
`count: 0` and `results: []` (not an error).

### Response `200 OK`

```json
{
  "count": 32,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "sku": "MN-AH-P",
      "name": "After Hours - Eau de Parfum",
      "slug": "after-hours-eau-de-parfum",
      "price": "590.00",
      "category": { "id": 1, "name": "Fine Fragrances", "slug": "fine-fragrances" },
      "collection": { "id": 1, "name": "After Hours", "slug": "after-hours" },
      "primary_image": null,
      "in_stock": true,
      "stock_quantity": 8
    }
  ]
}
```

`next` / `previous` are full URLs of the neighbouring pages, or `null`.

---

## GET `/api/products/{slug}/`

### Response `200 OK`

All `ProductSummary` fields, plus `description` and `images`:

```json
{
  "id": 1,
  "sku": "MN-AH-P",
  "name": "After Hours - Eau de Parfum",
  "slug": "after-hours-eau-de-parfum",
  "price": "590.00",
  "category": { "id": 1, "name": "Fine Fragrances", "slug": "fine-fragrances" },
  "collection": { "id": 1, "name": "After Hours", "slug": "after-hours" },
  "primary_image": null,
  "in_stock": true,
  "stock_quantity": 8,
  "description": "An eau de parfum of bergamot, iris and musk, composed for the late hours of a Parisian evening.",
  "images": []
}
```

With images, each image object looks like:

```json
{
  "id": 7,
  "image": "http://localhost:8000/media/products/after-hours-bottle.jpg",
  "alt_text": "After Hours eau de parfum bottle",
  "is_primary": true
}
```

### Response `404 Not Found`

Unknown slug, or the product is inactive:

```json
{ "detail": "No Product matches the given query." }
```

---

## GET `/api/categories/`

### Response `200 OK`

```json
[
  { "id": 1, "name": "Fine Fragrances", "slug": "fine-fragrances", "description": "" },
  { "id": 2, "name": "Scented Candles", "slug": "scented-candles", "description": "" }
]
```

---

## GET `/api/collections/`

### Response `200 OK`

```json
[
  {
    "id": 1,
    "name": "After Hours",
    "slug": "after-hours",
    "description": "Bergamot, iris and musk, composed for the late hours of a Parisian evening.",
    "launch_year": 2026
  }
]
```

`description` and `launch_year` come from the ER model's COLLECTIONS entity.

---

## Errors

| Status | When | Body |
|---|---|---|
| `404` | Unknown or inactive product slug | `{"detail": "..."}` |
| `405` | Any method other than `GET` / `HEAD` / `OPTIONS` | `{"detail": "Method \"POST\" not allowed."}` |
| `5xx` / network error | Backend or database down | Show a generic "could not load" message with a retry |
