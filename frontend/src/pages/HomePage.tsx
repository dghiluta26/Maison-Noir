import { Link } from 'react-router'
import { ProductCard } from '../components/catalog/ProductCard'
import { ProductGrid, ProductGridSkeleton } from '../components/catalog/ProductGrid'
import { useAsync } from '../hooks/useAsync'
import { getProducts } from '../services/catalogService'
import { isLimitedEdition, pickSignatureSelection } from '../utils/catalog'

const SIGNATURE_COUNT = 4

/**
 * Homepage — section order follows the Brand & P1 Project Book, "Homepage structure".
 * Sections still to come: Explore Our Universe (category pages), A Parisian State of Mind
 * and Our Philosophy (editorial content).
 */
export function HomePage() {
  const products = useAsync(getProducts, [])
  const all = products.status === 'success' ? products.data.results : []
  const limitedEditions = all.filter(isLimitedEdition)

  return (
    <>
      <title>MAISON NOIR — The Art of Living Beautifully</title>

      {/* Hero */}
      <section className="bg-espresso text-ivory">
        <div className="page-container flex min-h-[min(60vh,40rem)] flex-col items-start justify-center py-20 sm:py-28">
          <p className="text-xs font-semibold tracking-brand text-champagne uppercase">
            Parisian Fragrance &amp; Living
          </p>
          <h1 className="mt-6 max-w-3xl text-5xl leading-[1.05] text-ivory sm:text-7xl">
            The Art of Living Beautifully
          </h1>
          <p className="mt-6 max-w-xl text-base leading-relaxed text-taupe">
            Fragrance for the body, candles and reed diffusers for the home, and a small selection
            of sculptural objects — inspired by Parisian interiors and niche perfumery.
          </p>
          <Link to="/products" className="btn mt-10 bg-ivory text-espresso hover:bg-champagne">
            Discover the collection
          </Link>
        </div>
      </section>

      {/* Signature Selection */}
      <section className="page-container py-16 sm:py-24">
        <div className="mb-10 flex items-end justify-between gap-4">
          <div>
            <p className="eyebrow">Curated for you</p>
            <h2 className="mt-3 text-3xl sm:text-4xl">Signature Selection</h2>
          </div>
          <Link to="/products" className="eyebrow border-b border-espresso pb-1 hover:text-burgundy">
            View all
          </Link>
        </div>

        {products.status === 'loading' && <ProductGridSkeleton count={SIGNATURE_COUNT} />}
        {products.status === 'success' && (
          <ProductGrid products={pickSignatureSelection(all, SIGNATURE_COUNT)} />
        )}
        {/* On error the section is simply empty; the Shop page shows the full error state. */}
      </section>

      {/* Limited Editions */}
      {limitedEditions.length > 0 && (
        <section className="bg-ivory-deep py-16 sm:py-24">
          <div className="page-container grid items-center gap-12 lg:grid-cols-[1fr_2fr]">
            <div>
              <p className="text-xs font-semibold tracking-[0.18em] text-burgundy uppercase">
                Strictly limited
              </p>
              <h2 className="mt-3 text-3xl sm:text-4xl">Limited Editions</h2>
              <p className="mt-4 max-w-sm text-sm leading-relaxed text-espresso-soft">
                Only two MAISON NOIR collections are offered as gift sets, each produced in very
                small numbers.
              </p>
            </div>
            <ul className="grid grid-cols-2 gap-x-4 gap-y-10 sm:gap-x-6">
              {limitedEditions.map((product) => (
                <li key={product.id}>
                  <ProductCard product={product} />
                </li>
              ))}
            </ul>
          </div>
        </section>
      )}
    </>
  )
}
