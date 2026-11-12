# MAISON NOIR

**Parisian Fragrance & Living**

MAISON NOIR is a premium e-commerce project developed for the **E-Commerce Semester Project, Academic Year 2026–2027**.

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
├── components/   # layout (Header, Footer), catalog (ProductCard, grid), auth (AuthCard, RequireAuth) and ui building blocks
├── context/      # AuthProvider: the logged-in user for the whole app (read it with useAuth())
├── pages/        # one component per route
├── services/     # the only layer that talks to the API (catalogue, auth, API errors)
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

Status values:

- **Done**: implemented and merged into `main`
- **To do**: still has to be done before Presentation 2
- **Planned**: scheduled after Presentation 2

The full plan, with dependencies and handovers, is in `P2_Implementation_Execution_Plan.md`.

### Presentation 2: prototype

| No. | Task | Assigned to | Status |
|---:|---|---|---|
| 0.1 | Agree the final catalogue, product fields, initial API shape and ERD draft | Alexia + Denis | Done |
| 0.2 | Create the GitHub repository, invite the collaborator, configure branch protection and the issue board | Denis | Done |
| 0.3 | Create the repository structure, `.gitignore`, `.env.example`, initial README and Docker Compose | Denis | Done |
| 0.4 | Initialise Django, DRF, the PostgreSQL connection and the health endpoint | Denis | Done |
| 1.1 | Initialise React + TypeScript and create the base folders | Alexia | Done |
| 1.2 | Create the MAISON NOIR design tokens, layout, Header, Footer and route skeleton | Alexia | Done |
| 1.3 | Build `ProductCard`, the catalogue grid and the product page with temporary mock data | Alexia | Done |
| 2.1 | Create the custom `User` model and the `users` and `catalog` apps | Denis | Done |
| 2.2 | Implement `Category`, `Collection`, `Product`, `ProductImage`, constraints and migrations | Denis | Done |
| 2.3 | Implement the repeatable `seed_catalogue` command for the 32 products | Denis | Done |
| 2.4 | Implement and document the catalogue endpoints | Denis | Done |
| 2.5 | Connect the catalogue and product pages to the live API and remove the mock data | Alexia | Done |
| 2.6 | Resolve integration feedback: serializers, queries, product images, CORS, missing fields | Denis | To do |
| 3.1 | Decide and document the JWT auth contract | Denis | Done |
| 3.2 | Build the Register and Login pages, form validation and header states (no live calls) | Alexia | Done |
| 3.3 | Implement the auth endpoints, password handling, JWT configuration, permissions and tests | Denis | Done |
| 3.4 | Connect the forms to the auth API: header state, logout, redirects, protected `/account` page | Alexia | Done (PR awaiting review) |
| 3.5 | Fix auth integration issues and block customers from admin-only endpoints | Denis | To do |
| 4.1 | Fresh-clone setup test: containers, migrations, seed, backend, frontend | Denis (Alexia repeats it) | To do |
| 4.2 | Test the responsive UI (360 px), loading and error states, and the P2 demo path | Alexia | To do |
| 4.3 | Complete the baseline automated tests and update the README and API documentation | Denis | To do |
| 4.4 | Merge the approved PRs, rehearse the demo and tag `P2` | Alexia + Denis | To do |

### After Presentation 2

| No. | Task | Requirement | Assigned to | Status |
|---:|---|---|---|---|
| 5.1 | Filtered search and sorting | A2, B1 | Denis (API) + Alexia (UI) | Planned |
| 5.2 | Persistent cart and delivery methods | A3 | Alexia | Planned |
| 5.3 | Wishlist | B7 | Alexia + Denis | Planned |
| 5.4 | Orders, discount codes and checkout | A5, B5 | Alexia | Planned |
| 5.5 | Stripe test mode and webhook processing | A6, A7 | Alexia | Planned |
| 5.6 | Transactional email through Mailtrap | B6 | Alexia + Denis | Planned |
| 5.7 | Reviews and ratings, restricted to verified purchases | B3 | Alexia + Denis | Planned |
| 5.8 | Admin management and sales dashboard | A9, B4 | Denis | Planned |
| 5.9 | Recommendations based on category, collection and order data | B2 | Alexia + Denis | Planned |
| 5.10 | Accessibility, responsiveness, security checks and more test coverage | A10, A11, A12 | Alexia + Denis | Planned |

---

## AI Tools Used

As the course rules require, the team declares the AI tools used in this project. Every team member reviewed the AI-assisted work and can explain the resulting code.

| Tool | Used for |
|---|---|
| **Claude** (Anthropic, through Claude Code) | Help with code and implementation: writing and reviewing code, debugging, setting up the local environment, and drafting documentation |
| **Gemini** (Google) | Generating the product images for the catalogue |

---

## Authors

**Alexia Dinca**  
Frontend & Full-Stack Developer

**Denis Ghiluta**  
Backend & Database Developer
