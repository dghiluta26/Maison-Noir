/**
 * Minimal HTTP helper for the Django REST API.
 * Every failure is turned into an ApiError so the UI can handle it uniformly:
 *   - server unreachable (network error) -> status 0
 *   - non-2xx response                    -> the HTTP status code
 *   - 400 validation errors               -> also `fieldErrors` ({"field": ["msg", ...]})
 */
import { ApiError, type FieldErrors } from './errors'

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? '').replace(/\/+$/, '')

export interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'
  /** Sent as JSON. */
  body?: unknown
  /** Access token, sent as `Authorization: Bearer <token>`. */
  token?: string | null
  /** Send and store cookies (needed for the httpOnly refresh cookie on /api/auth/). */
  withCredentials?: boolean
}

/**
 * Performs a request to `{VITE_API_BASE_URL}{path}` and parses the JSON body.
 * Resolves with `undefined` for responses without a body (e.g. 204 No Content).
 */
export async function apiRequest<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { method = 'GET', body, token, withCredentials = false } = options

  const headers: Record<string, string> = { Accept: 'application/json' }
  if (body !== undefined) headers['Content-Type'] = 'application/json'
  if (token) headers.Authorization = `Bearer ${token}`

  let response: Response
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      method,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
      credentials: withCredentials ? 'include' : 'same-origin',
    })
  } catch {
    throw new ApiError('Could not reach the server. Please try again.', 0)
  }

  const data = await readJson(response)

  if (!response.ok) {
    throw new ApiError(errorMessage(response.status, data), response.status, fieldErrors(response.status, data))
  }

  return data as T
}

/** Performs a GET request to `{VITE_API_BASE_URL}{path}` and parses the JSON body. */
export function apiGet<T>(path: string): Promise<T> {
  return apiRequest<T>(path)
}

/** Parsed JSON body, or undefined when the body is empty or not JSON. */
async function readJson(response: Response): Promise<unknown> {
  if (response.status === 204) return undefined
  try {
    return await response.json()
  } catch {
    return undefined
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

/** Uses DRF's `{"detail": "..."}` message when present, otherwise a generic one. */
function errorMessage(status: number, data: unknown): string {
  if (isRecord(data) && typeof data.detail === 'string') return data.detail
  if (status === 400) return 'Please correct the highlighted fields.'
  return `Request failed (HTTP ${status}).`
}

/** DRF validation errors (400): keeps only `field -> list of messages` entries. */
function fieldErrors(status: number, data: unknown): FieldErrors {
  if (status !== 400 || !isRecord(data)) return {}
  const errors: FieldErrors = {}
  for (const [field, messages] of Object.entries(data)) {
    if (Array.isArray(messages)) {
      errors[field] = messages.filter((message): message is string => typeof message === 'string')
    } else if (typeof messages === 'string') {
      errors[field] = [messages]
    }
  }
  return errors
}
