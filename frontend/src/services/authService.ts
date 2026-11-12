/**
 * Authentication service — the ONLY place the UI talks to the auth API.
 * Contract: docs/api/auth.md.
 *
 * TEMPORARY (task 3.2): an in-memory stand-in that returns exactly the
 * responses and errors described in the contract, so the forms and header
 * states can be built without live calls. In task 3.4 the function bodies are
 * replaced with real requests (`credentials: 'include'` for the refresh cookie);
 * the signatures stay the same, so pages and the AuthProvider do not change.
 *
 * Stand-in limits: accounts and the session live in memory, so a page reload
 * logs you out and forgets accounts registered in this tab.
 * Demo accounts (stand-in only):
 *   demo.customer@example.com / Maison-Noir-26  (role: customer)
 *   demo.admin@example.com    / Maison-Noir-26  (role: admin)
 */
import type { AuthResponse, LoginPayload, RegisterPayload, User } from '../types/auth'
import { ApiError, type FieldErrors } from './errors'

/** Access token, kept in memory only (never localStorage). Used by API calls in task 3.4. */
let accessToken: string | null = null

export function getAccessToken(): string | null {
  return accessToken
}

export async function register(payload: RegisterPayload): Promise<AuthResponse> {
  await stubDelay()
  const email = payload.email.trim().toLowerCase()

  const errors: FieldErrors = {}
  if (stubAccounts.has(email)) {
    errors.email = ['An account with this email already exists.']
  }
  if (payload.password.length < 8) {
    errors.password = ['This password is too short. It must contain at least 8 characters.']
  }
  if (Object.keys(errors).length > 0) {
    throw new ApiError('Please correct the highlighted fields.', 400, errors)
  }

  const user: User = {
    id: stubNextId++,
    email,
    first_name: payload.first_name.trim(),
    last_name: payload.last_name.trim(),
    phone_number: payload.phone_number?.trim() ?? '',
    role: 'customer',
  }
  stubAccounts.set(email, { user, password: payload.password })
  return startSession(user)
}

export async function login(payload: LoginPayload): Promise<AuthResponse> {
  await stubDelay()
  const account = stubAccounts.get(payload.email.trim().toLowerCase())
  if (!account || account.password !== payload.password) {
    throw new ApiError('Invalid email or password.', 401)
  }
  return startSession(account.user)
}

/** Restores the session from the refresh cookie (called when the app starts). */
export async function refresh(): Promise<AuthResponse> {
  await stubDelay()
  const account = stubSessionEmail ? stubAccounts.get(stubSessionEmail) : undefined
  if (!account) {
    throw new ApiError('Session expired. Please log in again.', 401)
  }
  return startSession(account.user)
}

/** Always succeeds (the API returns 204 even when not logged in). */
export async function logout(): Promise<void> {
  await stubDelay()
  stubSessionEmail = null
  accessToken = null
}

// --- In-memory stand-in (removed in task 3.4) -------------------------------

const STUB_DELAY_MS = 400

interface StubAccount {
  user: User
  password: string
}

const stubAccounts = new Map<string, StubAccount>([
  [
    'demo.customer@example.com',
    {
      user: { id: 1, email: 'demo.customer@example.com', first_name: 'Claire', last_name: 'Martin', phone_number: '', role: 'customer' },
      password: 'Maison-Noir-26',
    },
  ],
  [
    'demo.admin@example.com',
    {
      user: { id: 2, email: 'demo.admin@example.com', first_name: 'Admin', last_name: 'Maison', phone_number: '', role: 'admin' },
      password: 'Maison-Noir-26',
    },
  ],
])

let stubNextId = 3
/** Stands in for the httpOnly refresh cookie. */
let stubSessionEmail: string | null = null

function startSession(user: User): AuthResponse {
  stubSessionEmail = user.email
  accessToken = `stub-access-token-${user.id}`
  return { access: accessToken, user }
}

function stubDelay(): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, STUB_DELAY_MS))
}
