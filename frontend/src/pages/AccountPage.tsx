import { useNavigate } from 'react-router'
import { StatusMessage } from '../components/ui/StatusMessage'
import { useAsync } from '../hooks/useAsync'
import { useAuth } from '../hooks/useAuth'
import { getMe } from '../services/authService'
import { isUnauthorized } from '../services/errors'
import type { User } from '../types/auth'

/** Profile of the logged-in user (protected by <RequireAuth>). Loaded from GET /api/auth/me/. */
export function AccountPage() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const me = useAsync(() => getMe(), [user?.id])

  async function handleSignOut() {
    navigate('/')
    await logout()
  }

  if (me.status === 'loading') {
    return (
      <div className="page-container py-20 text-center text-sm text-espresso-soft" role="status">
        Loading your account…
      </div>
    )
  }

  if (me.status === 'error') {
    // 401: the session is over; the AuthProvider is already logged out and
    // <RequireAuth> redirects to the sign-in page.
    if (isUnauthorized(me.error)) return null

    return (
      <div className="page-container">
        <StatusMessage
          role="alert"
          title="We couldn't load your account"
          action={
            <button type="button" className="btn-outline" onClick={me.retry}>
              Try again
            </button>
          }
        >
          Please check your connection and try again.
        </StatusMessage>
      </div>
    )
  }

  return <AccountView user={me.data} onSignOut={() => void handleSignOut()} />
}

function AccountView({ user, onSignOut }: { user: User; onSignOut: () => void }) {
  const details = [
    { label: 'Name', value: `${user.first_name} ${user.last_name}` },
    { label: 'Email', value: user.email },
    { label: 'Phone', value: user.phone_number || 'Not provided' },
    { label: 'Account type', value: user.role === 'admin' ? 'Administrator' : 'Customer' },
  ]

  return (
    <div className="page-container py-12 sm:py-20">
      <title>My account — MAISON NOIR</title>

      <div className="mx-auto max-w-xl">
        <p className="eyebrow">My account</p>
        <h1 className="mt-3 text-4xl">Bonjour, {user.first_name}</h1>

        <dl className="mt-10 divide-y divide-line border-y border-line">
          {details.map(({ label, value }) => (
            <div key={label} className="grid gap-1 py-4 sm:grid-cols-3 sm:gap-4">
              <dt className="eyebrow">{label}</dt>
              <dd className="text-sm text-espresso sm:col-span-2">{value}</dd>
            </div>
          ))}
        </dl>

        <button type="button" className="btn-outline mt-10" onClick={onSignOut}>
          Sign out
        </button>
      </div>
    </div>
  )
}
