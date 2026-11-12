/**
 * Authentication service — the ONLY place the UI talks to the auth API.
 * Contract: docs/api/auth.md.
 *
 *   POST /api/auth/register/  -> 201 {access, user} + refresh cookie
 *   POST /api/auth/login/     -> 200 {access, user} + refresh cookie
 *   POST /api/auth/refresh/   -> 200 {access, user} + new (rotated) refresh cookie
 *   POST /api/auth/logout/    -> 204, cookie deleted
 *
 * The access token lives in memory only (never localStorage). The refresh token
 * is an httpOnly cookie the browser handles for us, so every call here uses
 * `withCredentials` (fetch `credentials: 'include'`).
 * Failures are raised as ApiError (see ./errors).
 */
import type { AuthResponse, LoginPayload, RegisterPayload } from '../types/auth'
import { apiRequest } from './apiClient'

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
