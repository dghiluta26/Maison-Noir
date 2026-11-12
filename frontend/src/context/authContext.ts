import { createContext } from 'react'
import type { LoginPayload, RegisterPayload, User } from '../types/auth'

/**
 * - loading:       checking for an existing session when the app starts
 * - authenticated: `user` is set
 * - anonymous:     not logged in
 */
export type AuthStatus = 'loading' | 'authenticated' | 'anonymous'

export interface AuthContextValue {
  status: AuthStatus
  user: User | null
  /** Rejects with ApiError (401 wrong credentials, 400 validation, 0 network). */
  login: (payload: LoginPayload) => Promise<User>
  /** Rejects with ApiError (400 validation, 0 network). Logs the new user in. */
  register: (payload: RegisterPayload) => Promise<User>
  /** Never rejects; the user is always logged out locally. */
  logout: () => Promise<void>
}

export const AuthContext = createContext<AuthContextValue | null>(null)
