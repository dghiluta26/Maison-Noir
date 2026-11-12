# Authentication API (contract)

**Status:** agreed contract for P2 (task 3.1), **implemented in the backend** (task 3.3,
`backend/apps/users/`) and **connected in the frontend** (tasks 3.2 and 3.4:
`frontend/src/services/authService.ts`, `context/AuthProvider.tsx`, `components/auth/RequireAuth.tsx`).

Base URL (local): `http://localhost:8000/api/auth`

## Decisions

| Topic | Decision |
|---|---|
| Mechanism | JWT with access + refresh tokens (`djangorestframework-simplejwt`) |
| Login identifier | Email (case-insensitive) + password |
| Access token | Returned in the JSON body. Lifetime **15 minutes**. Kept **in memory only** in the frontend (never `localStorage`). Sent as `Authorization: Bearer <access>` |
| Refresh token | Never in the JSON body. Set by the backend in an **httpOnly cookie**, so JavaScript cannot read it. Lifetime **7 days**. **Rotated** on every refresh; the old one is blacklisted |
| Registration | Logs the user in immediately (same response as login) |
| Logout | Blacklists the refresh token and deletes the cookie |
| Staying logged in after a page reload | On app start the frontend calls `POST /refresh/`; if it succeeds the user is logged in again |
| Roles | `customer` (every registered account) and `admin` (created only with `createsuperuser` or in the Django admin; never through the API) |
| Passwords | Hashed by Django (PBKDF2); validated with Django's password validators |

### Refresh cookie

| Attribute | Value |
|---|---|
| Name | `mn_refresh` |
| `HttpOnly` | yes |
| `SameSite` | `Lax` |
| `Secure` | no on `http://localhost`; **yes** in production (HTTPS) |
| `Path` | `/api/auth/` (only sent to auth endpoints) |
| `Max-Age` | 7 days |

`http://localhost:5173` (Vite) and `http://localhost:8000` (Django) count as the
**same site**, so the cookie works locally. Always use `localhost`, never mix it
with `127.0.0.1`.

### Frontend requirements

- Every call to `/api/auth/register/`, `/login/`, `/refresh/` and `/logout/` must use
  `fetch(..., { credentials: 'include' })`, otherwise the browser neither stores
  nor sends the cookie.
- The backend enables `CORS_ALLOW_CREDENTIALS` for the origins in `CORS_ALLOWED_ORIGINS`.
- When an authenticated request returns `401`, call `POST /refresh/` **once**,
  then retry the request with the new access token. If the refresh also returns
  `401`, the session is over: clear the user and show the logged-out state.
- Catalogue endpoints stay public; they never need a token.

---

## User object

Returned by register, login, refresh and `me`:

```json
{
  "id": 3,
  "email": "ana.pop@example.com",
  "first_name": "Ana",
  "last_name": "Pop",
  "phone_number": "",
  "role": "customer"
}
```

`role` is `"customer"` or `"admin"`. Use it to show admin-only UI; the backend
still enforces permissions on every admin endpoint.

---

## POST `/api/auth/register/`

Creates a **customer** account and logs it in.

### Request

```json
{
  "email": "ana.pop@example.com",
  "password": "Parfum-de-nuit-26",
  "first_name": "Ana",
  "last_name": "Pop",
  "phone_number": "+40712345678"
}
```

| Field | Required | Rules |
|---|---|---|
| `email` | yes | valid email, not already registered (stored lowercase) |
| `password` | yes | at least 8 characters, not entirely numeric, not a common password, not too similar to the email or name |
| `first_name` | yes | max 150 characters |
| `last_name` | yes | max 150 characters |
| `phone_number` | no | max 20 characters |

A `role` field in the request is **ignored**; new accounts are always `customer`.
"Confirm password" is checked in the frontend form only; it is not sent.

### Response `201 Created`

```json
{
  "access": "eyJhbGciOiJIUzI1NiIs...",
  "user": { "id": 3, "email": "ana.pop@example.com", "first_name": "Ana", "last_name": "Pop", "phone_number": "+40712345678", "role": "customer" }
}
```

Plus header `Set-Cookie: mn_refresh=...; HttpOnly; SameSite=Lax; Path=/api/auth/`.

### Response `400 Bad Request` (validation)

Field errors, each a list of messages (show them under the matching inputs):

```json
{
  "email": ["An account with this email already exists."],
  "password": ["This password is too short. It must contain at least 8 characters."]
}
```

---

## POST `/api/auth/login/`

### Request

```json
{ "email": "ana.pop@example.com", "password": "Parfum-de-nuit-26" }
```

### Response `200 OK`

Same body and cookie as register.

### Response `401 Unauthorized`

Wrong email, wrong password or deactivated account. The message is
deliberately the same in all cases, so it doesn't reveal which emails exist:

```json
{ "detail": "Invalid email or password." }
```

### Response `400 Bad Request`

Missing fields: `{"email": ["This field is required."]}`.

---

## POST `/api/auth/refresh/`

No body. The browser sends the `mn_refresh` cookie automatically.

### Response `200 OK`

```json
{
  "access": "eyJhbGciOiJIUzI1NiIs...",
  "user": { "id": 3, "email": "ana.pop@example.com", "first_name": "Ana", "last_name": "Pop", "phone_number": "", "role": "customer" }
}
```

Plus a **new** `mn_refresh` cookie (rotation). The previous refresh token stops working.

### Response `401 Unauthorized`

No cookie, or the token is expired, invalid or already used/blacklisted. Treat this as "not logged in":

```json
{ "detail": "Session expired. Please log in again." }
```

---

## POST `/api/auth/logout/`

No body; uses the cookie.

### Response `204 No Content`

The refresh token is blacklisted and the cookie is deleted. Always returns
`204`, even if the user was not logged in, so logout can never fail in the UI.
The frontend must also drop the access token from memory.

---

## GET `/api/auth/me/`

Header: `Authorization: Bearer <access>`

### Response `200 OK`

The user object.

### Response `401 Unauthorized`

No token:

```json
{ "detail": "Authentication credentials were not provided." }
```

Invalid or expired token (the JWT library adds `code` and `messages`; rely only
on the `401` status and `detail`):

```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [{ "token_class": "AccessToken", "token_type": "access", "message": "Token is invalid" }]
}
```

---

## Roles and permissions

| Who | Catalogue (`GET /api/products/` …) | `GET /api/auth/me/` | Admin-only endpoints (added in task 3.5 and later) |
|---|---|---|---|
| Visitor (not logged in) | ✅ | `401` | `401` |
| Customer | ✅ | ✅ | `403` |
| Admin | ✅ | ✅ | ✅ |

`403` body: `{"detail": "You do not have permission to perform this action."}`

Backend: protect an endpoint with `permission_classes = [IsAdminRole]`
(`apps.users.permissions`). Public endpoints (catalogue, auth entry points)
ignore the `Authorization` header, so an expired token never breaks them.

---

## Error format summary

| Status | Meaning | Body | Frontend action |
|---|---|---|---|
| `400` | Validation failed | `{"<field>": ["msg", ...]}`, or `{"non_field_errors": ["msg"]}` | Show messages next to the fields |
| `401` | Not logged in / bad credentials / session expired | `{"detail": "msg"}` | Login form: show `detail`. Other requests: refresh once, else log out |
| `403` | Logged in but not allowed (customer on admin endpoint) | `{"detail": "msg"}` | Show "not allowed" message |
| `5xx` / network error | Backend unavailable | — | Generic error with retry |

## Out of scope for P2

Password reset, email verification, social login and login rate limiting are
not part of P2. They can be added later without changing the endpoints above.
