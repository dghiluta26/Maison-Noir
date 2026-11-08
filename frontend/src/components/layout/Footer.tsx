import { Link } from 'react-router'

const CURRENT_YEAR = new Date().getFullYear()

export function Footer() {
  return (
    <footer className="mt-24 bg-espresso text-ivory">
      <div className="page-container grid gap-10 py-14 sm:grid-cols-2 lg:grid-cols-4">
        <div className="lg:col-span-2">
          <p className="font-serif text-2xl tracking-brand">MAISON NOIR</p>
          <p className="mt-3 font-serif text-xl text-champagne italic">
            The Art of Living Beautifully
          </p>
          <p className="mt-3 max-w-sm text-sm leading-relaxed text-taupe">
            Parisian fragrance &amp; living — fine fragrances, scented candles, home fragrance and
            design objects.
          </p>
        </div>

        <nav aria-label="Shop">
          <p className="text-xs font-semibold tracking-[0.18em] text-champagne uppercase">Shop</p>
          <ul className="mt-4 space-y-2 text-sm">
            <li>
              <Link to="/products" className="hover:text-champagne">
                All products
              </Link>
            </li>
          </ul>
        </nav>

        <nav aria-label="Account">
          <p className="text-xs font-semibold tracking-[0.18em] text-champagne uppercase">Account</p>
          <ul className="mt-4 space-y-2 text-sm">
            <li>
              <Link to="/login" className="hover:text-champagne">
                Sign in
              </Link>
            </li>
            <li>
              <Link to="/register" className="hover:text-champagne">
                Create an account
              </Link>
            </li>
          </ul>
        </nav>
      </div>

      <div className="border-t border-white/10">
        <p className="page-container py-5 text-xs text-taupe">
          © {CURRENT_YEAR} MAISON NOIR — academic e-commerce project. Not a real store.
        </p>
      </div>
    </footer>
  )
}
