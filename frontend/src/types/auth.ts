/**
 * Authentication types — mirror docs/api/auth.md (snake_case, as the API sends them).
 */

export type Role = 'customer' | 'admin'

/** User object returned by register, login, refresh and me. */
export interface User {
  id: number
  email: string
  first_name: string
  last_name: string
  phone_number: string
  role: Role
}

/** Body of a successful register / login / refresh response. */
export interface AuthResponse {
  /** Short-lived access token; kept in memory only. */
  access: string
  user: User
}

/** POST /api/auth/login/ */
export interface LoginPayload {
  email: string
  password: string
}

/** POST /api/auth/register/ ("confirm password" is checked in the form only). */
export interface RegisterPayload {
  email: string
  password: string
  first_name: string
  last_name: string
  phone_number?: string
}
