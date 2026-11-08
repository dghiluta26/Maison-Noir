import { Link } from 'react-router'
import type { ProductSummary } from '../../types/catalog'
import { isLimitedEdition, isLowStock } from '../../utils/catalog'
import { formatPrice } from '../../utils/format'
import { ProductImageFrame } from './ProductImageFrame'

interface ProductCardProps {
  product: ProductSummary
}

const badgeBase =
  'absolute top-3 left-3 px-2.5 py-1 text-[0.65rem] font-semibold tracking-[0.16em] uppercase'

/** One label per card, most important first. */
function ProductBadge({ product }: ProductCardProps) {
  if (!product.in_stock) {
    return <span className={`${badgeBase} bg-espresso text-ivory`}>Sold out</span>
  }
  if (isLimitedEdition(product)) {
    return <span className={`${badgeBase} bg-burgundy text-ivory`}>Limited Edition</span>
  }
  if (isLowStock(product)) {
    return (
      <span className={`${badgeBase} border border-champagne bg-ivory text-espresso`}>
        Only {product.stock_quantity} left
      </span>
    )
  }
  return null
}

export function ProductCard({ product }: ProductCardProps) {
  return (
    <article className="group">
      <Link to={`/products/${product.slug}`} className="block">
        <div className="relative">
          <ProductImageFrame
            image={product.primary_image}
            productName={product.name}
            className="transition-opacity duration-300 group-hover:opacity-90"
          />
          <ProductBadge product={product} />
        </div>

        <div className="mt-4 space-y-1">
          <p className="eyebrow">{product.category.name}</p>
          <h3 className="font-serif text-xl leading-snug transition-colors group-hover:text-burgundy">
            {product.name}
          </h3>
          {product.collection && (
            <p className="text-sm text-espresso-soft">{product.collection.name}</p>
          )}
          <p className="pt-1 text-sm font-semibold">{formatPrice(product.price)}</p>
        </div>
      </Link>
    </article>
  )
}
