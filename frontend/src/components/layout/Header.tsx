import { Link, NavLink } from 'react-router'

const navLinkClass = ({ isActive }: { isActive: boolean }) =>
  [
    'eyebrow border-b py-1 transition-colors hover:text-burgundy',
    isActive ? 'border-burgundy text-espresso' : 'border-transparent',
  ].join(' ')

export function Header() {
  return (
    <header className="sticky top-0 z-40 border-b border-line bg-ivory/95 backdrop-blur-sm">
      <div className="page-container flex h-16 items-center justify-between gap-4 sm:h-20">
        <Link
          to="/"
          className="font-serif text-xl tracking-brand whitespace-nowrap text-espresso sm:text-2xl"
          aria-label="MAISON NOIR — home"
        >
          MAISON NOIR
        </Link>

        <nav aria-label="Main" className="flex items-center gap-5 sm:gap-8">
          <NavLink to="/products" className={navLinkClass}>
            Shop
          </NavLink>
          {/* Authenticated header states are added in task 3.2 / 3.4. */}
          <NavLink to="/login" className={navLinkClass}>
            Sign in
          </NavLink>
        </nav>
      </div>
    </header>
  )
}
