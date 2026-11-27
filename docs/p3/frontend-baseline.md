# P3 Frontend Baseline (Task 0.1)

**Owner:** Alexia Dinca
**Reviewer:** Denis Ghiluta
**Date:** 27 November 2026
**Branch:** `docs/p3-frontend-audit`, based on `main` at `1f414a0`
**Scope:** Read-only audit of `frontend/` and of the backend contract the frontend uses. No application code was changed.

## 1. Build, lint and smoke results

| Check | Command | Result |
|---|---|---|
| Type check + production build | `npm run build` (in `frontend/`) | Passed, 132 modules, JS 358.7 kB (110.7 kB gzip), CSS 40.3 kB |
| Lint | `npm run lint` (oxlint) | Passed, exit code 0, no findings |
| Frontend tests | none | No test runner configured (no Vitest, RTL or Playwright) |
| Dev server | `npm run dev` | Served on `http://localhost:5173` |
| Backend for smoke | `python manage.py runserver 8000`, DB container `maison_noir_db` healthy | All migrations applied |

### API smoke (as consumed by the frontend)

| Request | Status | Observation |
|---|---|---|
| `GET /api/health/` | 200 | |
| `GET /api/categories/` | 200 | 5 categories, plain list |
| `GET /api/collections/` | 200 | 13 collections, plain list (not used by the frontend yet) |
| `GET /api/products/` | 200 | count 32, all 32 on one page (default page size 48) |
| `GET /api/products/?page_size=24` / `&page=2` | 200 | 24 + 8, pagination envelope works |
| `GET /api/products/?search=candle` | 200 | 16 results: search also matches description, SKU, category and collection |
| `GET /api/products/?search=zzzz` | 200 | 0 results |
| `GET /api/products/?category=fine-fragrances` | 200 | 7 results |
| `GET /api/products/does-not-exist/` | 404 | |
| `GET /api/auth/me/` (no token) | 401 | |
| `GET /api/admin/products/` (no token) | 401 | |

Category slugs: `fine-fragrances`, `scented-candles`, `home-fragrance`, `design-objects`, `limited-gift-sets`.
Collection slugs: `after-hours`, `golden-hour`, `midnight-in-paris`, `fleur-de-minuit`, `cafe-creme`, `paris-after-dark`, `maison-blanche`, `soft-linen`, `ambre-parisien`, `l-appartement`, `chambre-noire`, `fleur-de-maison`, `santal-residence`.

### Route smoke

Every path returns the SPA shell (HTTP 200) from Vite; routing happens in the browser.

| Route | Component | Access | State |
|---|---|---|---|
| `/` | HomePage | Public | Working: hero, Signature Selection, Limited Editions |
| `/products` | CataloguePage | Public | Working: lists all products; no search, filters or paging controls |
| `/products/:slug` | ProductDetailPage | Public | Working: gallery, price, stock; "Add to bag" disabled |
| `/login`, `/register` | LoginPage, RegisterPage | Public | Working: live auth, safe `from` redirect |
| `/account` | AccountPage (inside RequireAuth) | Customer | Profile live; Favourites and Orders tabs use mock data |
| `*` | NotFoundPage | Public | Working; `/cart`, `/checkout`, `/admin` currently land here |

## 2. Stack and tooling

- React 19.3, React Router 8.5 (`createBrowserRouter`), TypeScript 7.0, Vite 8.3, Tailwind CSS 4.3 (`@tailwindcss/vite`), oxlint 1.90.
- Fonts: `@fontsource-variable/cormorant-garamond`, `@fontsource-variable/manrope`.
- `vite.config.ts` reads env from the repository root (`envDir: '..'`), dev port 5173 with `strictPort`.
- Only `VITE_API_BASE_URL` is read by the frontend.
- Scripts: `dev`, `build`, `lint`, `preview`. No `test` script.

## 3. Design system (source of truth: `frontend/src/styles/index.css`)

- Brand colours: ivory `#F7F4EF`, espresso `#2A211E`, burgundy `#641F32`, champagne `#C5A77B`, taupe `#B8A99A`.
- Mixed tones: `cream` (page background, champagne 24% into ivory), `ivory-deep`, `sand`, `espresso-soft`, `line`.
- Fonts: `font-serif` (Cormorant Garamond) for h1 to h3, `font-sans` (Manrope) for the body.
- Utilities: `page-container`, `eyebrow`, `btn`, `btn-primary`, `btn-outline`.
- Motion: `animate-slide-in-right` and `animate-fade-up`, used only with `motion-safe:`.
- Global `:focus-visible` outline in burgundy.
- No hard-coded hex values were found in components.

## 4. Code inventory

| Area | Files | Notes |
|---|---|---|
| Routing | `router.tsx` | Single layout route; `RequireAuth` wraps `/account` only |
| Layout | `Layout.tsx`, `Header.tsx`, `Footer.tsx` | Header: Shop, Account or Sign in, Sign out. No cart or favourites entry |
| Catalogue UI | `ProductCard`, `ProductGrid` (+ skeleton), `ProductImageFrame` | Reusable; badges for sold out, limited edition, low stock (threshold 3) |
| Shared UI | `StatusMessage`, `FormField`, `AuthCard` | Used for loading, empty and error states |
| Hooks | `useAsync`, `useAuth`, `useScrolledPast` | `useAsync` handles loading, error and retry and ignores stale responses |
| Auth | `AuthProvider`, `authContext`, `authService`, `RequireAuth`, `utils/authForms` | Access token in memory; refresh cookie; single shared refresh; one 401 retry; safe relative redirect |
| HTTP | `apiClient.ts`, `errors.ts` | JSON only, `ApiError` with status and DRF field errors |
| Catalogue data | `catalogService.ts`, `types/catalog.ts`, `utils/catalog.ts` | `getCategories`, `getProducts()` (no parameters), `getProduct(slug)` |
| Account data | `accountService.ts`, `mocks/account.ts`, `types/account.ts`, `OrderHistory.tsx` | Favourites and orders built from mocks plus live products |
| Assets | `assets/home-parisian-living-room.jpg`, `public/` logo and favicons | Product photography is served by the backend media folder |

## 5. Gaps found (mapped to P3 tasks)

| # | Gap | Affected files | P3 task |
|---|---|---|---|
| G1 | `getProducts()` takes no query parameters; no `getCollections`, no category or collection fetch by slug | `catalogService.ts` | 1.2 |
| G2 | Catalogue has no search box, paging controls, or category/collection pages | `CataloguePage.tsx`, `router.tsx` | 1.2 |
| G3 | HomePage, `pickSignatureSelection` and `accountService` assume every product fits on one page. When the page size becomes 24 (task 1.1), Limited Editions and favourites can disappear | `HomePage.tsx`, `utils/catalog.ts`, `accountService.ts` | 1.2 (with Denis 1.1) |
| G4 | `ProductDetail` type and page ignore the fields the API already returns: `tagline`, `size`, `burn_time`, `includes`, `notes_top/heart/base`, `materials`, `edition`, `ritual` | `types/catalog.ts`, `ProductDetailPage.tsx` | 1.2 |
| G5 | Breadcrumb category is plain text, not a link | `ProductDetailPage.tsx` | 1.2 |
| G6 | No cart: "Add to bag" is disabled, no cart context, no `/cart` route, no header count | `ProductDetailPage.tsx`, `Header.tsx` | 1.5, 3.5 |
| G7 | No addresses UI or service | `AccountPage.tsx` | 1.6 |
| G8 | No checkout, success or cancel routes | `router.tsx` | 2.3, 2.5 |
| G9 | Order history and favourites use mock data. Mock delivery values (Standard "2-3 days", Express 40 RON) contradict the P3 rules (Standard 25 RON 3-5 days, Express 45 RON 1-2 days) | `mocks/account.ts`, `accountService.ts`, `types/account.ts` | 3.1, 4.7 |
| G10 | No dedicated `/account/orders`, `/account/orders/:number`, `/account/addresses`, `/account/favourites` routes; tabs use `?tab=` | `AccountPage.tsx`, `router.tsx` | 1.6, 3.1, 4.7 |
| G11 | `apiClient` always JSON-encodes the body; FormData uploads are not supported | `apiClient.ts` | 3.4 |
| G12 | No admin area: no role guard, layout or pages; admins only see an "Admin" label in the header | `router.tsx`, `Header.tsx` | 3.4 |
| G13 | Footer always shows "Sign in" and "Create an account", even for signed-in users; only one shop link | `Footer.tsx` | 3.5 |
| G14 | No frontend test tooling | `package.json` | 5.2 |
| G15 | No frontend Dockerfile | `frontend/` | 5.3a |

## 6. Notes for task 0.3 (contract agreement with Denis)

1. **Pagination (1.1):** after the change to 24, the homepage needs either a filtered request (for example `?category=limited-gift-sets`) or a small "featured" endpoint. Please confirm the filter stays available.
2. **Search (A2):** the backend searches name, description, SKU, category and collection. "candle" returns 16 products. Confirm this broader search is acceptable for A2, or whether name matches should be ranked first.
3. **Category and collection detail:** the frontend needs either `GET /categories/{slug}/` and `GET /collections/{slug}/`, or it filters the list responses. The collection list already returns `description`, `tagline`, `story`, `image`, `launch_year`.
4. **Order shape:** the frontend draft (`types/account.ts`) uses `number`, `placed_at`, `status`, `delivery_method`, `delivery_cost`, `items[{product, quantity, unit_price, line_total}]`, `subtotal`, `total`. The final order API should also return item snapshots (name, SKU, image), payment state, address snapshot and discount. Agree on these fields in 0.3.
5. **Statuses:** the frontend uses lower-case `new | paid | shipped | delivered | cancelled`; please keep the same values in the API.
6. **Errors:** the frontend already handles DRF `{"detail": ...}` and field-error objects. A stable `code` field for stock conflicts and invalid transitions (409) would let the UI show specific messages.
7. **SPA shell and admin:** in development every path serves `index.html`. Protecting `/admin` on the server (A10) must be designed together with the frontend container (5.3, 5.3a).
