import { useCallback, useEffect, useMemo, useState, type ReactNode } from 'react'
import * as authService from '../services/authService'
import type { LoginPayload, RegisterPayload, User } from '../types/auth'
import { AuthContext, type AuthContextValue, type AuthStatus } from './authContext'

interface AuthState {
  status: AuthStatus
  user: User | null
}

const ANONYMOUS: AuthState = { status: 'anonymous', user: null }

/** Holds the logged-in user for the whole app. Components read it with useAuth(). */
export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<AuthState>({ status: 'loading', user: null })

  // Restore an existing session (refresh cookie) when the app starts.
  useEffect(() => {
    let active = true
    authService.refresh().then(
      ({ user }) => active && setState({ status: 'authenticated', user }),
      () => active && setState(ANONYMOUS),
    )
    return () => {
      active = false
    }
  }, [])

  // An authenticated request found that the session is over (refresh failed).
  useEffect(() => authService.onSessionExpired(() => setState(ANONYMOUS)), [])

  const login = useCallback(async (payload: LoginPayload) => {
    const { user } = await authService.login(payload)
    setState({ status: 'authenticated', user })
    return user
  }, [])

  const register = useCallback(async (payload: RegisterPayload) => {
    const { user } = await authService.register(payload)
    setState({ status: 'authenticated', user })
    return user
  }, [])

  const logout = useCallback(async () => {
    try {
      await authService.logout()
    } catch {
      // Logging out must never fail in the UI; the local session is cleared below.
    } finally {
      setState(ANONYMOUS)
    }
  }, [])

  const value = useMemo<AuthContextValue>(
    () => ({ ...state, login, register, logout }),
    [state, login, register, logout],
  )

  return <AuthContext value={value}>{children}</AuthContext>
}
