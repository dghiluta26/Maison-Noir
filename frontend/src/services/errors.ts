/** Error raised by the service layer when a request fails. */
export class ApiError extends Error {
  /** HTTP status code, or 0 when the server could not be reached. */
  readonly status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

export function isNotFound(error: unknown): boolean {
  return error instanceof ApiError && error.status === 404
}
