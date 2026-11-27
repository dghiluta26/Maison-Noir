# P3 backend baseline (task 0.2)

**Owner:** Denis · **Reviewer:** Alexia · **Date:** 27 November 2026
**Base:** `main` at `1f414a0` (P2 accepted; tag `P2` preserved). Read-only audit: no code or data changed.

## Verified state

| Check | Command | Result |
|---|---|---|
| Database | `docker compose up -d db` | PostgreSQL 17 container healthy |
| Migrations applied | `python manage.py migrate` | No migrations to apply |
| Missing migrations | `python manage.py makemigrations --check --dry-run` | No changes detected |
| Dependencies | `pip check` | No broken requirements |
| Tests | `pytest` | **107 passed** (PostgreSQL test database) |
| Health | `GET /api/health/` | `{"status": "ok", "database": "ok"}` |
| Catalogue | `GET /api/products/` | 32 products, primary images served from `/media/` (HTTP 200) |

Tests per file: auth API 34 · catalogue API 18 · catalogue models 15 · admin API 13 · seed 11 · user model 10 · health 3 · password hashing 3.
(The P2 specification quoted 103; the 4 extra tests came with the seed texts and images.)

## Current backend

- **Apps:** `core` (health), `users` (custom User, email login, role customer/admin, JWT auth), `catalog` (Category, Collection, Product, ProductImage, seed, public and admin API).
- **Migrations:** `users` 0001; `catalog` 0001–0005 (P2 schema plus editorial fields, collection image, includes).
- **Routes:** `/api/health/`; `/api/categories/`, `/api/collections/`, `/api/products/` (+ detail by slug); `/api/auth/register|login|refresh|logout|me/`; `/api/admin/products/` (read-only, `IsAdminRole`); Django admin at `/admin/`.
- **Auth and security:** JWT (15 min access, 7 day rotating refresh in httpOnly cookie, `SameSite=Lax`, path `/api/auth/`, blacklist); Argon2 hashing; `IsAuthenticated` by default; public views opt out explicitly; CORS limited to `CORS_ALLOWED_ORIGINS` with credentials.
- **Dependencies:** Django 5.2.19, DRF 3.18.3, SimpleJWT 5.5.1, django-cors-headers 4.9.0, django-environ 0.14.0, Pillow 13.0.0, psycopg 3.3.8, argon2-cffi 25.1.0; dev: pytest 9.2.0, pytest-django 4.14.0.
- **Settings:** `base.py`, `development.py`, `test.py` (no production settings module).
- **Docker Compose:** only the `db` service.

## Gaps P3 must close (backend)

| # | Gap | Requirement | P3 task |
|---|---|---|---|
| 1 | Public page size is 48 (max 100); spec allows at most 24 per page | A1 | 1.1 |
| 2 | `seed_catalogue` uses `update_or_create`: every run resets price, stock, `is_active` and seed images, overwriting admin edits | A7, A9 | 1.1 |
| 3 | Search covers name, description, SKU, collection and category; spec requires correct results on product **names** (keep broader search only if results stay correct) | A2 | 1.1 |
| 4 | No `Address`, `DeliveryMethod` tables or endpoints | A4, A5 | 1.3 |
| 5 | No `Cart`, `CartItem`, `Order`, `OrderItem`, `Payment`, `WebhookEvent`, reservation tables | A3, A5–A8 | 1.4 |
| 6 | Stock is a single `stock_quantity`; no reservation, locking or exactly-once decrement | A7 | 2.1 |
| 7 | No order status machine or cancellation/refund logic | A7, A9 | 2.2, 2.6 |
| 8 | Admin API is read-only products; no product/category/collection CRUD, image upload, orders or customers | A9 | 3.2, 3.3 |
| 9 | Cookie endpoints (`refresh`, `logout`) rely on `SameSite=Lax` + CORS only; no explicit Origin/CSRF check | A10 | 3.6 |
| 10 | No request throttling on login/register | A10 (hardening) | 3.6 |
| 11 | No cart, total, payment or webhook tests yet (required by A12) | A12 | 2.x, 5.1 |
| 12 | Startup needs more than 5 commands (db, venv, pip, migrate, seed, runserver, npm install, npm run dev); Compose runs only `db` | Spec 2.1 | 5.3 |
| 13 | No reviews, discounts, dashboard or filter (price/availability/ordering) backend | B1, B3–B5 | 4.1, 4.4–4.6 |

## Notes for task 0.3

- Pagination change (gap 1) affects every frontend consumer that assumes all products fit on one page (homepage selections, catalogue). Coordinate with Alexia before merging 1.1.
- The seed change (gap 2) needs an explicit, separate "reset demo data" path for disposable databases only.
- Hosted Stripe Checkout differs from the frozen P2 flow (embedded PaymentIntent): written teacher approval needed before 2.4.
- Running locally requires Docker Desktop to be running first; otherwise `runserver` waits for the database with no error.
