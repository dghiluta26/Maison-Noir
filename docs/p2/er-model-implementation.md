# ER model → database implementation (P2)

The database follows the MAISON NOIR E-R model. This note records how each
entity is implemented and which **extensions** were added for the P2
storefront, so the ER diagram can be updated to match.

## Mapping

| ER entity | Table | Django model | Status |
|---|---|---|---|
| CUSTOMERS | `users` | `apps.users.User` | Implemented (task 2.1) |
| COLLECTIONS | `collections` | `apps.catalog.Collection` | Implemented (task 2.2) |
| PRODUCTS | `products` | `apps.catalog.Product` | Implemented (task 2.2) |
| ORDERS | — | — | After P2 |
| ORDER_ITEMS | — | — | After P2 |

| ER attribute | Implemented as |
|---|---|
| `customer_id`, `collection_id`, `product_id` | `id` primary key on each table |
| CUSTOMERS `first_name`, `last_name`, `email`, `phone_number` | same names; `email` is unique and used to log in |
| COLLECTIONS `collection_name` | `name` (unique) |
| COLLECTIONS `description`, `launch_year` | same names |
| PRODUCTS `collection_id` (FK) | `collection_id`, required (1:N "contains") |
| PRODUCTS `product_name` | `name` |
| PRODUCTS `product_type` | `category_id` → `categories` table (see extensions) |
| PRODUCTS `scent_description` | `description` |
| PRODUCTS `price` | `price` decimal(10,2), in lei, must be ≥ 0 |
| PRODUCTS `stock_quantity` | same name, must be ≥ 0 |

## Extensions (not in the ER model)

Agreed for P2 because the plan and the storefront need them:

| Extension | Why |
|---|---|
| `users.role` (`customer` / `admin`) + Django auth columns (`password`, `is_active`, …) | P2 requires the roles customer and admin; login needs a password hash |
| `categories` table (`name`, `slug`, `description`, `sort_order`) replacing `product_type` | 5 browsable categories; avoids repeating type names as free text |
| `products.sku` (unique) | Catalogue reference code, e.g. `MN-AH-P` |
| `products.slug`, `collections.slug`, `categories.slug` (unique) | Readable URLs: `GET /api/products/{slug}/` |
| `products.is_active` | Inactive products are hidden from the public storefront |
| `product_images` table (`image`, `alt_text`, `is_primary`, `sort_order`) | Product photos; at most one primary image per product |
| `sort_order` on categories and collections; `created_at` / `updated_at` | Display order and audit timestamps |

## Seed data

`python manage.py seed_catalogue` inserts 5 categories, 13 collections and
32 products, copied unchanged from the agreed catalogue
(`frontend/src/mocks/catalog.ts`). Collection `description` and
`launch_year` are draft values in `backend/apps/catalog/seed_data.py`.
