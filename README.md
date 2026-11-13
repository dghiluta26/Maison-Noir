# MAISON NOIR

**Parisian Fragrance & Living**

MAISON NOIR is a premium e-commerce project developed for the **E-Commerce Semester Project, Academic Year 2026-2027**.

The application represents a curated fragrance and lifestyle store inspired by Parisian luxury. The catalogue contains **32 products** across personal fragrances, scented candles, reed diffusers, design objects and limited gift sets.

The platform will support the complete online shopping flow: product browsing, search, shopping cart, user accounts, checkout, sandbox payments, stock management, order history and a custom administration panel.

---

## Team

### Alexia Dinca — Frontend & Full-Stack Developer

Primary responsibilities:
- React + TypeScript frontend
- UI/UX implementation
- product catalogue and product pages
- shopping cart
- checkout flow
- Stripe payment integration
- payment webhook handling
- order history
- responsive design
- selected Django REST API endpoints


### Denis Ghiluta — Backend & Database Developer

Primary responsibilities:
- Django + Django REST Framework backend
- PostgreSQL database
- authentication and authorization
- product search backend
- stock management
- database transactions
- custom administration backend
- application security
- automated testing


---

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React + TypeScript |
| Build Tool | Vite |
| Styling | Tailwind CSS |
| Backend | Python + Django + Django REST Framework |
| Database | PostgreSQL |
| ORM | Django ORM |
| Payments | Stripe Test Mode |
| Email Testing | Mailtrap |
| Backend Testing | pytest + pytest-django |
| Frontend Testing | Vitest + React Testing Library |
| End-to-End Testing | Playwright |
| Local Environment | Docker Compose |
| Version Control | GitHub |

The administration panel will be custom built in React and connected to secured Django REST API endpoints.

---

## Project Scope

The store will include:

- product catalogue with category pages
- product detail pages
- text search
- shopping cart
- user registration and authentication
- saved delivery address
- checkout with multiple delivery methods
- Stripe sandbox payment flow
- webhook-based payment confirmation
- stock management
- customer order history
- custom administration dashboard
- responsive design
- automated tests

The product catalogue contains **32 SKUs** organised into fragrance and home-lifestyle collections such as:

- After Hours
- Golden Hour
- Café Crème
- Paris After Dark
- Soft Linen
- Ambre Parisien

Main product categories:

- Fine Fragrances
- Scented Candles
- Reed Diffusers / Home Fragrance
- Design Objects
- Limited Gift Sets

---

## Brand Identity

**Style:** Parisian Luxury / Quiet Luxury

**Color palette:**

| Color | HEX |
|---|---|
| Ivory | `#F7F4EF` |
| Espresso | `#2A211E` |
| Burgundy | `#641F32` |
| Champagne | `#C5A77B` |
| Warm Taupe | `#B8A99A` |

**Typography:**
- Cormorant Garamond — headings
- Manrope — body text and interface

---

## Repository Structure

```text
maison-noir/
├── backend/             # Django + Django REST Framework API
├── frontend/            # React + TypeScript storefront (Vite)
├── docs/
│   ├── api/             # API contract and JSON examples
│   ├── diagrams/        # ERD and architecture diagrams
│   └── p2/              # Presentation 2 specification and decisions
├── docker-compose.yml   # Local PostgreSQL service
├── .env.example         # Template for local environment variables
└── README.md
```

---

## Local Setup

### Prerequisites

- Git
- Docker Desktop (with Docker Compose v2)
- Python 3.12+
- Node.js 20+ (for the frontend)

### 1. Clone the repository

```bash
git clone <repository-url>
cd Maison-Noir
```

### 2. Create your local environment file

```bash
cp .env.example .env
```

Edit `.env` and set your own local values (at minimum `POSTGRES_PASSWORD` and `DJANGO_SECRET_KEY`). The `.env` file is ignored by Git and must never be committed.

### 3. Start PostgreSQL

```bash
docker compose up -d db
docker compose ps        # STATUS should show "healthy"
```

Useful commands:

```bash
docker compose logs -f db      # follow database logs
docker compose down            # stop the database (data is kept)
docker compose down -v         # stop and DELETE all local database data
```

### 4. Backend (Django + DRF)

Create a virtual environment and install the dependencies:

```powershell
# Windows (PowerShell)
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

```bash
# macOS / Linux
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

With PostgreSQL running (step 3), create the database tables:

```bash
python manage.py migrate
```

Load the catalogue (5 categories, 13 collections, 32 products):

```bash
python manage.py seed_catalogue
```

The command is safe to run repeatedly: it updates existing rows (matched by slug / SKU) instead of creating duplicates, and resets them to the seed values. The seed data lives in `backend/apps/catalog/seed_data.py`.

Optionally, create an admin account for the Django admin at http://localhost:8000/admin/ (you will be asked for email, first name, last name and password):

```bash
python manage.py createsuperuser
```

Users log in with their **email address**. Every account has a role: `customer` (default for new accounts) or `admin` (given automatically to superusers).

The authentication API (`/api/auth/register/`, `login/`, `refresh/`, `logout/`, `me/`) uses JWT: a short-lived access token in the response body and the refresh token in an httpOnly cookie. See `docs/api/auth.md`.

Start the API:

```bash
python manage.py runserver
```

Check that it works by opening http://localhost:8000/api/health/. Expected response:

```json
{"status": "ok", "database": "ok"}
```

If PostgreSQL is not reachable, the endpoint returns HTTP `503` with `{"status": "error", "database": "unavailable"}`.

Run the backend tests (from `backend/`, with the virtual environment active and PostgreSQL running):

```bash
pytest
```

> After pulling changes that include new migrations, run `python manage.py migrate` again.

### 5. Frontend (React + TypeScript + Vite)

The frontend reads `VITE_API_BASE_URL` from the same root `.env` file created in step 2. Only variables prefixed with `VITE_` are exposed to the browser.

Install the dependencies and start the development server:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. The port is fixed to `5173` because it must match `CORS_ALLOWED_ORIGINS` in `.env`.

Other commands (run from `frontend/`):

```bash
npm run build     # type-check (tsc) and build the production bundle into frontend/dist
npm run preview   # serve the production build locally
npm run lint      # lint the source code with oxlint
```

Frontend structure:

```text
frontend/src/
├── components/   # layout (Header, Footer), catalog (ProductCard, grid), auth (AuthCard, RequireAuth), account (OrderHistory) and ui building blocks
├── context/      # AuthProvider: the logged-in user for the whole app (read it with useAuth())
├── mocks/        # TEMPORARY sample favourites/orders for the account preview; only accountService imports it
├── pages/        # one component per route
├── services/     # the only layer that talks to the API (catalogue, auth, account, API errors)
├── hooks/        # reusable React hooks (e.g. useAsync for loading/error states)
├── types/        # TypeScript interfaces mirroring the REST API responses
├── styles/       # Tailwind CSS entry point and MAISON NOIR design tokens
├── utils/        # formatting helpers (prices) and auth form validation
├── router.tsx    # route definitions
└── main.tsx      # application entry point
```

> Catalogue data is loaded from the Django REST API at `VITE_API_BASE_URL` (root `.env`) through `src/services/catalogService.ts`, which uses the shared request helper in `src/services/apiClient.ts`. Pages never call `fetch` directly. See `docs/api/catalogue.md` for the API contract.

> Authentication (sign in, register, sign out, `/account`) uses the live auth API through `src/services/authService.ts`; see `docs/api/auth.md` for the contract. The access token is kept in memory only and the refresh token in an httpOnly cookie, so the session survives a page reload. Requests that need a logged-in user go through `authRequest()`, which refreshes the access token once on `401` and retries. Pages that need a logged-in user are wrapped in `<RequireAuth>` (see `src/router.tsx`).
>
> Open the app at **http://localhost:5173**, not `127.0.0.1`: the refresh cookie only works when the frontend and the API are both on `localhost`. To test the admin role, create an account with `python manage.py createsuperuser`.

---

## Task Plan and Status

The tasks follow the requirement codes of the course's Project Specification (section 2.2 for A1–A12, section 2.3 for B1–B7). Owners are those agreed in the P1 presentation (6 mandatory requirements each).

Status values:

- **Done**: fully implemented and merged into `main`
- **In progress**: partly implemented; the status says what is still missing
- **Planned**: not started yet, scheduled for P3

### Mandatory requirements (A1–A12)

| No. | Task | Assigned to | Status |
|---:|---|---|---|
| A1 | Product catalogue: paginated product list (at most 24 products per page), a page for each category, and a product page with name, description, price, images and availability | Alexia | In progress: product page and product list done; missing category pages and 24-per-page pagination |
| A2 | Basic search: text search on product names with correct results and a clear message when nothing is found | Denis | In progress: backend search (`?search=`) done; missing the search box and "no results" message in the storefront |
| A3 | Shopping cart: add, update and remove products; total recalculated on the server; quantities above stock rejected; an authenticated user's cart persists after logout | Alexia | Planned |
| A4 | User accounts: registration, login and logout, passwords stored with bcrypt or Argon2, at least one saved delivery address | Denis | In progress: registration, login, logout and Argon2 done; missing saved delivery address |
| A5 | Checkout: address, delivery method (at least two, with different costs), order summary and payment; confirmation page with the order number | Alexia | Planned |
| A6 | Sandbox payment: an order becomes Paid only on the payment processor's confirmation (Stripe webhook), not the browser redirect; a failed payment leaves it Unpaid | Alexia | Planned |
| A7 | Stock management: stock decreases when payment is confirmed and is restored when an order is cancelled; two customers cannot buy the last unit at the same time | Denis | Planned |
| A8 | Order history: customers see their orders with date, products, total and status | Alexia | In progress: account page design with sample orders; missing the orders API |
| A9 | Administration panel: separate admin role; product and category CRUD with image upload; order list filterable by status with transitions New → Paid → Shipped → Delivered, or Cancelled | Denis | In progress: admin role and admin products API done; missing category CRUD, orders and the React admin panel |
| A10 | Basic security: server-side validation, CSRF protection, ORM or parameterised queries; admin pages and API endpoints blocked on the server for regular users | Denis | In progress: validation, ORM and server-side admin blocking (403) done; to be extended to every new endpoint |
| A11 | Responsive design: all customer-facing pages usable on a 360 px wide screen | Alexia | In progress: current pages are mobile-first; to be checked for every new page |
| A12 | Automated tests: at least 10 tests, run with a single command, covering at least the cart, total calculation and payment confirmation | Denis | In progress: 107 backend tests run with `pytest`; missing cart, total and payment tests |

### Bonus features (B1–B7)

| No. | Task | Points | Assigned to | Status |
|---:|---|---|---|---|
| B1 | Filtered search: combinable filters by category, price range and availability, sorting by price and date added, filters kept in the URL | 5 | Not assigned | Planned |
| B2 | Recommendations: "Similar products" or "Frequently bought together", computed from data (category, attributes or orders) | 4 | Not assigned | Planned |
| B3 | Reviews and ratings: only buyers can review; average rating in the catalogue; administrators can hide a review | 4 | Not assigned | Planned |
| B4 | Sales dashboard: daily sales chart, top 5 products and average order value for a selected time interval | 3 | Not assigned | Planned |
| B5 | Discount codes: percentage or fixed amount, with expiry date and maximum number of uses, validated on the server | 3 | Not assigned | Planned |
| B6 | Transactional email: order confirmation email sent through Mailtrap | 5 | Not assigned | Planned |
| B7 | Wishlist: favourites list for authenticated users, with the option to move items to the cart | 2 | Not assigned | In progress: account page design with sample favourites; missing the wishlist API |

Bonus points count only once A1–A12 work, up to a maximum of 20. Order of work agreed at P2: B1, B6, B2, B3, then B4, B5, B7.

---

## AI Tools Used

As the course rules require, the team declares the AI tools used in this project. Every team member reviewed the AI-assisted work and can explain the resulting code.

| Tool | Used for |
|---|---|
| **Claude** (Anthropic, through Claude Code) | Help with code and implementation: writing and reviewing code, debugging, setting up the local environment, and drafting documentation |
| **ChatGPT** (OpenAI) | Generating the product and collection images for the catalogue |

---

## Authors

**Alexia Dinca**  
Frontend & Full-Stack Developer

**Denis Ghiluta**  
Backend & Database Developer
