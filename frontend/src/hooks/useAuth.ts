import { useContext } from 'react'
import { AuthContext, type AuthContextValue } from '../context/authContext'

/** Current user and auth actions. Must be used inside <AuthProvider>. */
export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used inside <AuthProvider>.')
  }
  return context
}
