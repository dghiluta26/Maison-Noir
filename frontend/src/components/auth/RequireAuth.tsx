import { Navigate, Outlet, useLocation } from 'react-router'
import { useAuth } from '../../hooks/useAuth'

/**
 * Layout route for pages that need a logged-in user.
 * Visitors are sent to /login and come back here after signing in. This also
 * covers a session that expires while the page is open (the AuthProvider
 * switches to "anonymous" and this redirects).
 */
export function RequireAuth() {
  const { status } = useAuth()
  const location = useLocation()

  if (status === 'loading') {
    // The session is still being restored from the refresh cookie.
    return (
      <div className="page-container py-20 text-center text-sm text-espresso-soft" role="status">
        Loading…
      </div>
    )
  }

  if (status === 'anonymous') {
    return <Navigate to="/login" replace state={{ from: `${location.pathname}${location.search}` }} />
  }

  return <Outlet />
}
