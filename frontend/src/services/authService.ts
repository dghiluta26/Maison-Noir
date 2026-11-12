/**
 * Authentication service — the ONLY place the UI talks to the auth API.
 * Contract: docs/api/auth.md.
 *
 *   POST /api/auth/register/  -> 201 {access, user} + refresh cookie
 *   POST /api/auth/login/     -> 200 {access, user} + refresh cookie
 *   POST /api/auth/refresh/   -> 200 {access, user} + new (rotated) refresh cookie
 *   POST /api/auth/logout/    -> 204, cookie deleted
 *   GET  /api/auth/me/        -> 200 user (needs the access token)
 *
 * The access token lives in memory only (never localStorage). The refresh token
 * is an httpOnly cookie the browser handles for us, so every call to the auth
 * entry points uses `withCredentials` (fetch `credentials: 'include'`).
 * Endpoints that need a logged-in user are called through authRequest().
 * Failures are raised as ApiError (see ./errors).
 */
import type { AuthResponse, LoginPayload, RegisterPayload, User } from '../types/auth'
import { apiRequest, type RequestOptions } from './apiClient'
import { isUnauthorized } from './errors'

/** Access token, kept in memory only. Lost on page reload; restored by refresh(). */
let accessToken: string | null = null

export function getAccessToken(): string | null {
  return accessToken
}

export async function register(payload: RegisterPayload): Promise<AuthResponse> {
  return startSession(
    apiRequest<AuthResponse>('/auth/register/', { method: 'POST', body: payload, withCredentials: true }),
  )
}

export async function login(payload: LoginPayload): Promise<AuthResponse> {
  return startSession(
    apiRequest<AuthResponse>('/auth/login/', { method: 'POST', body: payload, withCredentials: true }),
  )
}

/** A refresh request that is still running; shared by everyone who asks meanwhile. */
let refreshInFlight: Promise<AuthResponse> | null = null

/**
 * Gets a new access token from the refresh cookie (used when the app starts and
 * when an access token has expired). Rejects with a 401 ApiError when there is
 * no valid session.
 *
 * Concurrent calls share one request: the backend rotates the refresh token, so
 * a second parallel request would send a cookie that was just invalidated and
 * end the session (this happens on every reload in dev, where StrictMode runs
 * the startup effect twice).
 */
export function refresh(): Promise<AuthResponse> {
  refreshInFlight ??= startSession(
    apiRequest<AuthResponse>('/auth/refresh/', { method: 'POST', withCredentials: true }),
  ).finally(() => {
    refreshInFlight = null
  })
  return refreshInFlight
}

/** Always succeeds locally: the token is dropped even if the request fails. */
export async function logout(): Promise<void> {
  accessToken = null
  await apiRequest<void>('/auth/logout/', { method: 'POST', withCredentials: true })
}

/** The logged-in user's profile. */
export function getMe(): Promise<User> {
  return authRequest<User>('/auth/me/')
}

// --- Authenticated requests ---------------------------------------------------

type SessionExpiredListener = () => void

const sessionExpiredListeners = new Set<SessionExpiredListener>()

/**
 * Registers a callback for when the session ends on its own (refresh token
 * expired or revoked). Returns an unsubscribe function.
 */
export function onSessionExpired(listener: SessionExpiredListener): () => void {
  sessionExpiredListeners.add(listener)
  return () => {
    sessionExpiredListeners.delete(listener)
  }
}

/**
 * Request to an endpoint that needs a logged-in user (contract: docs/api/auth.md).
 * Sends the access token; on 401 (usually an expired access token) it calls
 * refresh() ONCE and retries with the new token. If the refresh also fails with
 * 401, the session is over: the token is cleared, listeners are notified and
 * the 401 ApiError is raised. Other errors (403, network...) are raised as-is.
 */
export async function authRequest<T>(path: string, options: Omit<RequestOptions, 'token'> = {}): Promise<T> {
  try {
    return await apiRequest<T>(path, { ...options, token: accessToken })
  } catch (error) {
    if (!isUnauthorized(error)) throw error
  }

  try {
    await refresh()
  } catch (error) {
    if (isUnauthorized(error)) {
      sessionExpiredListeners.forEach((listener) => listener())
    }
    throw error
  }

  return apiRequest<T>(path, { ...options, token: accessToken })
}

/** Stores the access token from a successful response; clears it on failure. */
async function startSession(request: Promise<AuthResponse>): Promise<AuthResponse> {
  try {
    const response = await request
    accessToken = response.access
    return response
  } catch (error) {
    accessToken = null
    throw error
  }
}
