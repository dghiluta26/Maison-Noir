import type { ProductSummary } from '../../types/catalog'
import { ProductCard } from './ProductCard'

const gridClass = 'grid grid-cols-2 gap-x-4 gap-y-10 sm:gap-x-6 lg:grid-cols-3 xl:grid-cols-4'

export function ProductGrid({ products }: { products: ProductSummary[] }) {
  return (
    <ul className={gridClass}>
      {products.map((product) => (
        <li key={product.id}>
          <ProductCard product={product} />
        </li>
      ))}
    </ul>
  )
}

/** Placeholder grid shown while products are loading. */
export function ProductGridSkeleton({ count = 8 }: { count?: number }) {
  return (
    <div role="status" aria-label="Loading products">
      <ul className={gridClass} aria-hidden="true">
        {Array.from({ length: count }, (_, i) => (
          <li key={i} className="animate-pulse">
            <div className="aspect-[4/5] bg-ivory-deep" />
            <div className="mt-4 h-3 w-1/3 bg-ivory-deep" />
            <div className="mt-3 h-5 w-3/4 bg-ivory-deep" />
            <div className="mt-3 h-4 w-1/4 bg-ivory-deep" />
          </li>
        ))}
      </ul>
    </div>
  )
}
