/**
 * Minimal HTTP helper for the Django REST API.
 * Every failure is turned into an ApiError so the UI can handle it uniformly:
 *   - server unreachable (network error) -> status 0
 *   - non-2xx response                    -> the HTTP status code
 */
import { ApiError } from './errors'

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? '').replace(/\/+$/, '')

/** Performs a GET request to `{VITE_API_BASE_URL}{path}` and parses the JSON body. */
export async function apiGet<T>(path: string): Promise<T> {
  let response: Response
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      headers: { Accept: 'application/json' },
    })
  } catch {
    throw new ApiError('Could not reach the server. Please try again.', 0)
  }

  if (!response.ok) {
    throw new ApiError(await errorMessage(response), response.status)
  }

  return (await response.json()) as T
}

/** Uses DRF's `{"detail": "..."}` message when present, otherwise a generic one. */
async function errorMessage(response: Response): Promise<string> {
  try {
    const body: unknown = await response.json()
    if (body && typeof body === 'object' && 'detail' in body && typeof body.detail === 'string') {
      return body.detail
    }
  } catch {
    // Body is not JSON; fall through to the generic message.
  }
  return `Request failed (HTTP ${response.status}).`
}
