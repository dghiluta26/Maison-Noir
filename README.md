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

With PostgreSQL running (step 3), start the API:

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

> Database migrations are introduced together with the custom user model in a later step. Until then, `runserver` shows an "unapplied migrations" warning. This is expected; do **not** run `migrate` yet.

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
├── components/   # layout (Header, Footer), catalog (ProductCard, grid) and ui building blocks
├── pages/        # one component per route
├── services/     # the only layer that fetches data (catalogue service, API errors)
├── hooks/        # reusable React hooks (e.g. useAsync for loading/error states)
├── types/        # TypeScript interfaces mirroring the REST API responses
├── styles/       # Tailwind CSS entry point and MAISON NOIR design tokens
├── utils/        # formatting helpers (prices)
├── mocks/        # TEMPORARY mock catalogue, removed when the live API is connected
├── router.tsx    # route definitions
└── main.tsx      # application entry point
```

> Until the catalogue API is available, the storefront uses temporary mock data from `src/mocks/catalog.ts` through `src/services/catalogService.ts`. Pages never import mock data directly.

---

## Authors

**Alexia Dinca**  
Frontend & Full-Stack Developer

**Denis Ghiluta**  
Backend & Database Developer
