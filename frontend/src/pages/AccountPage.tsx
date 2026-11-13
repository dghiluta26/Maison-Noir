import type { ReactNode } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router'
import { OrderHistory, OrderStatusBadge } from '../components/account/OrderHistory'
import { ProductGrid, ProductGridSkeleton } from '../components/catalog/ProductGrid'
import { StatusMessage } from '../components/ui/StatusMessage'
import { useAsync } from '../hooks/useAsync'
import { useAuth } from '../hooks/useAuth'
import { getAccountActivity } from '../services/accountService'
import { getMe } from '../services/authService'
import { isUnauthorized } from '../services/errors'
import type { AccountActivity } from '../types/account'
import type { User } from '../types/auth'

const TABS = [
  { id: 'profile', label: 'Profile' },
  { id: 'favourites', label: 'Favourites' },
  { id: 'orders', label: 'Order history' },
] as const

type TabId = (typeof TABS)[number]['id']

/**
 * The customer's account (protected by <RequireAuth>).
 * Profile: live data from GET /api/auth/me/.
 * Favourites and order history: PREVIEW with mock data (see accountService).
 * The open section is kept in the URL (?tab=orders) so links and Back work.
 */
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
  const [searchParams] = useSearchParams()
  const requested = searchParams.get('tab')
  const tab: TabId = TABS.some((t) => t.id === requested) ? (requested as TabId) : 'profile'

  const activity = useAsync(() => getAccountActivity(), [user.id])
  const counts: Partial<Record<TabId, number>> =
    activity.status === 'success'
      ? { favourites: activity.data.favourites.length, orders: activity.data.orders.length }
      : {}

  return (
    <div>
      <title>My account — MAISON NOIR</title>

      <AccountHeader user={user} onSignOut={onSignOut} />

      <div className="page-container py-10 sm:py-14">
        <nav aria-label="Account sections" className="-mx-4 overflow-x-auto px-4 sm:mx-0 sm:px-0">
          <ul className="flex min-w-max gap-8 border-b border-line">
            {TABS.map(({ id, label }) => {
              const active = id === tab
              return (
                <li key={id}>
                  <Link
                    to={id === 'profile' ? '/account' : `/account?tab=${id}`}
                    aria-current={active ? 'page' : undefined}
                    className={`-mb-px inline-flex items-center gap-2 border-b-2 pb-3 text-xs font-semibold tracking-[0.18em] uppercase transition-colors ${
                      active ? 'border-burgundy text-espresso' : 'border-transparent text-espresso-soft hover:text-burgundy'
                    }`}
                  >
                    {label}
                    {counts[id] !== undefined && <span className="text-champagne">{counts[id]}</span>}
                  </Link>
                </li>
              )
            })}
          </ul>
        </nav>

        <div className="mt-10">
          {tab === 'profile' && <ProfilePanel user={user} activity={activity.status === 'success' ? activity.data : null} />}
          {tab !== 'profile' && (
            <>
              <PreviewNote />
              {activity.status === 'loading' && (tab === 'favourites' ? <ProductGridSkeleton count={4} /> : <OrdersSkeleton />)}
              {activity.status === 'error' && (
                <StatusMessage
                  role="alert"
                  title="We couldn't load this section"
                  action={
                    <button type="button" className="btn-outline" onClick={activity.retry}>
                      Try again
                    </button>
                  }
                >
                  Please check your connection and try again.
                </StatusMessage>
              )}
              {activity.status === 'success' && tab === 'favourites' && <FavouritesPanel activity={activity.data} />}
              {activity.status === 'success' && tab === 'orders' && <OrderHistory orders={activity.data.orders} />}
            </>
          )}
        </div>
      </div>
    </div>
  )
}

/** Espresso band with the official logo, greeting and sign-out. */
function AccountHeader({ user, onSignOut }: { user: User; onSignOut: () => void }) {
  return (
    <section className="bg-espresso text-ivory">
      <div className="page-container flex flex-col gap-8 py-10 sm:flex-row sm:items-center sm:py-14">
        <img
          src="/maison-noir-logo.png"
          alt="MAISON NOIR logo"
          width={112}
          height={112}
          className="h-24 w-24 shrink-0 border border-champagne/30 sm:h-28 sm:w-28"
        />

        <div className="min-w-0 flex-1">
          <p className="eyebrow text-champagne">My account</p>
          <h1 className="mt-2 text-4xl text-ivory sm:text-5xl">Bonjour, {user.first_name}</h1>
          <p className="mt-3 flex flex-wrap items-center gap-x-3 gap-y-2 text-sm text-taupe">
            <span className="break-all">{user.email}</span>
            <span aria-hidden="true" className="h-3 w-px bg-champagne/40" />
            <span className="text-xs font-semibold tracking-[0.18em] text-champagne uppercase">
              {user.role === 'admin' ? 'Administrator' : 'Client'}
            </span>
          </p>
        </div>

        <button
          type="button"
          onClick={onSignOut}
          className="btn self-start border border-champagne/60 text-ivory hover:bg-champagne hover:text-espresso sm:self-center"
        >
          Sign out
        </button>
      </div>
    </section>
  )
}

function ProfilePanel({ user, activity }: { user: User; activity: AccountActivity | null }) {
  const details = [
    { label: 'First name', value: user.first_name },
    { label: 'Last name', value: user.last_name },
    { label: 'Email', value: user.email },
    { label: 'Phone', value: user.phone_number || 'Not provided' },
  ]
  const lastOrder = activity?.orders[0]

  return (
    <div className="grid gap-10 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)]">
      <section aria-labelledby="details-heading">
        <h2 id="details-heading" className="text-3xl">
          Personal details
        </h2>
        <dl className="mt-6 divide-y divide-line border-y border-line">
          {details.map(({ label, value }) => (
            <div key={label} className="grid gap-1 py-4 sm:grid-cols-3 sm:gap-4">
              <dt className="eyebrow">{label}</dt>
              <dd className="text-sm break-words text-espresso sm:col-span-2">{value}</dd>
            </div>
          ))}
        </dl>
      </section>

      <aside className="space-y-4">
        <SummaryCard
          title="Order history"
          to="/account?tab=orders"
          linkLabel="View orders"
          value={activity ? `${activity.orders.length} orders` : '…'}
        >
          {lastOrder && (
            <span className="flex items-center gap-2">
              Latest: {lastOrder.number} <OrderStatusBadge status={lastOrder.status} />
            </span>
          )}
        </SummaryCard>
        <SummaryCard
          title="Favourites"
          to="/account?tab=favourites"
          linkLabel="View favourites"
          value={activity ? `${activity.favourites.length} saved` : '…'}
        >
          Pieces you would like to return to.
        </SummaryCard>
      </aside>
    </div>
  )
}

function SummaryCard(props: { title: string; value: string; to: string; linkLabel: string; children?: ReactNode }) {
  return (
    <div className="border border-line bg-ivory p-6">
      <p className="eyebrow">{props.title}</p>
      <p className="mt-2 font-serif text-3xl">{props.value}</p>
      {props.children && <div className="mt-2 text-xs text-espresso-soft">{props.children}</div>}
      <Link to={props.to} className="mt-5 inline-block text-xs font-semibold tracking-[0.18em] text-burgundy uppercase hover:underline">
        {props.linkLabel}
      </Link>
    </div>
  )
}

function FavouritesPanel({ activity }: { activity: AccountActivity }) {
  if (activity.favourites.length === 0) {
    return (
      <div className="border border-line bg-ivory px-6 py-12 text-center">
        <p className="font-serif text-2xl">No favourites yet</p>
        <p className="mt-2 text-sm text-espresso-soft">Save the pieces you love and find them here later.</p>
        <Link to="/products" className="btn-primary mt-8">
          Discover the collections
        </Link>
      </div>
    )
  }
  return <ProductGrid products={activity.favourites} />
}

/** Honest label for the demo: these sections use sample data for now. */
function PreviewNote() {
  return (
    <p className="mb-8 border-l-2 border-champagne bg-ivory px-4 py-3 text-xs text-espresso-soft">
      <span className="font-semibold tracking-[0.18em] text-espresso uppercase">Preview</span> — this section shows
      sample data. Saving favourites and placing orders will be connected in a later release.
    </p>
  )
}

function OrdersSkeleton() {
  return (
    <div role="status" aria-label="Loading orders" className="space-y-4">
      {[0, 1, 2].map((i) => (
        <div key={i} className="h-20 animate-pulse border border-line bg-ivory-deep/40" />
      ))}
    </div>
  )
}
