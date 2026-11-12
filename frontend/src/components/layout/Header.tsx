import { Link, NavLink, useLocation } from 'react-router'
import { useAuth } from '../../hooks/useAuth'
import { useScrolledPast } from '../../hooks/useScrolledPast'

/** On the homepage the header appears after scrolling this many pixels. */
const HOME_REVEAL_OFFSET = 80

const navLinkClass = ({ isActive }: { isActive: boolean }) =>
  [
    'border-b py-1 text-xs font-semibold tracking-[0.18em] whitespace-nowrap uppercase transition-colors',
    isActive
      ? 'border-champagne text-ivory'
      : 'border-transparent text-taupe hover:text-champagne',
  ].join(' ')

export function Header() {
  const isHome = useLocation().pathname === '/'
  const scrolled = useScrolledPast(HOME_REVEAL_OFFSET)

  // Homepage: the header floats over the full-screen hero and is hidden until the
  // visitor scrolls. It also appears when it receives keyboard focus (focus-within).
  // Other pages: a normal sticky header, always visible.
  const position = isHome
    ? [
        'fixed inset-x-0 top-0 transition-[translate,opacity] duration-500',
        scrolled
          ? 'translate-y-0 opacity-100'
          : 'pointer-events-none -translate-y-full opacity-0 focus-within:pointer-events-auto focus-within:translate-y-0 focus-within:opacity-100',
      ].join(' ')
    : 'sticky top-0'

  return (
    <header className={`${position} z-40 border-b border-champagne/20 bg-espresso/95 backdrop-blur-sm`}>
      <div className="page-container flex h-16 items-center justify-between gap-4 sm:h-20">
        <Link
          to="/"
          className="font-serif text-lg tracking-[0.2em] whitespace-nowrap text-ivory sm:text-2xl sm:tracking-brand"
          aria-label="MAISON NOIR — home"
        >
          MAISON NOIR
        </Link>

        <nav aria-label="Main" className="flex items-center gap-4 sm:gap-8">
          <NavLink to="/products" className={navLinkClass}>
            Shop
          </NavLink>
          <AccountNav />
        </nav>
      </div>
    </header>
  )
}

/** Sign-in link for visitors; name and sign-out for logged-in users. */
function AccountNav() {
  const { status, user, logout } = useAuth()
  const location = useLocation()

  if (status === 'loading') {
    // Reserve the space while the session is being restored, to avoid a flicker.
    return <span aria-hidden="true" className="inline-block w-16" />
  }

  if (status === 'authenticated' && user) {
    return (
      <>
        <span className="hidden text-xs font-semibold tracking-[0.18em] whitespace-nowrap text-champagne uppercase md:inline">
          {user.first_name}
          {user.role === 'admin' && <span className="ml-2 text-taupe">· Admin</span>}
        </span>
        <button type="button" onClick={() => void logout()} className={navLinkClass({ isActive: false })}>
          Sign out
        </button>
      </>
    )
  }

  return (
    // Remember the current page so the visitor returns to it after signing in.
    <NavLink to="/login" state={{ from: location.pathname }} className={navLinkClass}>
      Sign in
    </NavLink>
  )
}
