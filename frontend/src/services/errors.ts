/** DRF validation errors: `{"field": ["message", ...]}` (HTTP 400). */
export type FieldErrors = Record<string, string[]>

/** Error raised by the service layer when a request fails. */
export class ApiError extends Error {
  /** HTTP status code, or 0 when the server could not be reached. */
  readonly status: number
  /** Per-field validation messages (only for 400 responses). */
  readonly fieldErrors: FieldErrors

  constructor(message: string, status: number, fieldErrors: FieldErrors = {}) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.fieldErrors = fieldErrors
  }
}

export function isNotFound(error: unknown): boolean {
  return error instanceof ApiError && error.status === 404
}

export function isUnauthorized(error: unknown): boolean {
  return error instanceof ApiError && error.status === 401
}
