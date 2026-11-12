# Admin API

Endpoints for the custom administration panel (spec A9). Every endpoint here
requires a logged-in user with role **`admin`** and is enforced **on the
server** (spec A10), not only hidden in the interface.

Base URL (local): `http://localhost:8000/api/admin`
Header: `Authorization: Bearer <access>` (see `docs/api/auth.md`)

| Who | Response |
|---|---|
| Visitor (no token / invalid token) | `401` `{"detail": "Authentication credentials were not provided."}` |
| Customer | `403` `{"detail": "You do not have permission to perform this action."}` |
| Admin | `200` |

Access depends on the user's `role`, not on Django's `is_staff` flag.
Backend: `permission_classes = [IsAdminRole]` (`apps.users.permissions`).

## Endpoints

| Method | Route | Access | Description |
|---|---|---|---|
| GET | `/api/admin/products/` | admin | All products, **including inactive** ones. Paginated like the public list. Query: `?search=`, `?is_active=true\|false`, `?page=`, `?page_size=` |
| GET | `/api/admin/products/{slug}/` | admin | One product, active or inactive |

Read-only in P2. Creating, editing and deleting products and categories
(with image upload) and the order list are added with the administration
panel after P2.

## Product object (admin)

All fields of the public product detail (`docs/api/catalogue.md`), plus:

| Field | Type | Description |
|---|---|---|
| `is_active` | boolean | `false` = hidden from the public storefront |
| `created_at` | ISO 8601 datetime | When the product was created |
| `updated_at` | ISO 8601 datetime | Last change |
