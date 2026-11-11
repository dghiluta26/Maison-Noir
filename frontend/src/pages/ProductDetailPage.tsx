import { useState } from 'react'
import { Link, useParams } from 'react-router'
import { ProductImageFrame } from '../components/catalog/ProductImageFrame'
import { StatusMessage } from '../components/ui/StatusMessage'
import { useAsync } from '../hooks/useAsync'
import { getProduct } from '../services/catalogService'
import { isNotFound } from '../services/errors'
import type { ProductDetail } from '../types/catalog'
import { isLimitedEdition, LOW_STOCK_THRESHOLD } from '../utils/catalog'
import { formatPrice } from '../utils/format'

export function ProductDetailPage() {
  const { slug = '' } = useParams()
  const product = useAsync(() => getProduct(slug), [slug])

  if (product.status === 'loading') {
    return <ProductDetailSkeleton />
  }

  if (product.status === 'error') {
    return isNotFound(product.error) ? (
      <div className="page-container">
        <title>Product not found — MAISON NOIR</title>
        <StatusMessage
          title="Product not found"
          action={
            <Link to="/products" className="btn-primary">
              Back to the shop
            </Link>
          }
        >
          This product does not exist or is no longer available.
        </StatusMessage>
      </div>
    ) : (
      <div className="page-container">
        <StatusMessage
          role="alert"
          title="We couldn't load this product"
          action={
            <button type="button" className="btn-outline" onClick={product.retry}>
              Try again
            </button>
          }
        >
          Please check your connection and try again.
        </StatusMessage>
      </div>
    )
  }

  // `key` resets the selected image when navigating between products.
  return <ProductDetailView key={product.data.slug} product={product.data} />
}

function ProductDetailView({ product }: { product: ProductDetail }) {
  const primaryIndex = Math.max(
    0,
    product.images.findIndex((img) => img.is_primary),
  )
  const [selectedIndex, setSelectedIndex] = useState(primaryIndex)
  const selectedImage = product.images[selectedIndex] ?? product.primary_image

  return (
    <div className="page-container py-8 sm:py-12">
      <title>{`${product.name} — MAISON NOIR`}</title>

      <nav aria-label="Breadcrumb" className="mb-8 text-xs text-espresso-soft">
        <ol className="flex flex-wrap items-center gap-2">
          <li>
            <Link to="/products" className="hover:text-burgundy">
              Shop
            </Link>
          </li>
          <li aria-hidden="true">/</li>
          <li>{product.category.name}</li>
          <li aria-hidden="true">/</li>
          <li aria-current="page" className="text-espresso">
            {product.name}
          </li>
        </ol>
      </nav>

      <div className="grid gap-10 md:grid-cols-2 lg:gap-16">
        <section aria-label="Product images">
          <ProductImageFrame image={selectedImage} productName={product.name} eager />

          {product.images.length > 1 && (
            <ul className="mt-4 grid grid-cols-5 gap-3">
              {product.images.map((img, index) => (
                <li key={img.id}>
                  <button
                    type="button"
                    onClick={() => setSelectedIndex(index)}
                    aria-label={`Show image ${index + 1} of ${product.images.length}`}
                    aria-pressed={index === selectedIndex}
                    className={`block w-full border transition-colors ${
                      index === selectedIndex ? 'border-espresso' : 'border-transparent hover:border-line'
                    }`}
                  >
                    <ProductImageFrame image={img} productName={product.name} />
                  </button>
                </li>
              ))}
            </ul>
          )}
        </section>

        <section className="md:pt-4">
          {isLimitedEdition(product) && (
            <p className="mb-4 inline-block bg-burgundy px-2.5 py-1 text-[0.65rem] font-semibold tracking-[0.16em] text-ivory uppercase">
              Limited Edition
            </p>
          )}
          <p className="eyebrow">
            {product.category.name}
            {product.collection && <> · {product.collection.name}</>}
          </p>
          <h1 className="mt-3 text-4xl leading-tight sm:text-5xl">{product.name}</h1>
          <p className="mt-5 text-xl font-semibold">{formatPrice(product.price)}</p>

          <StockStatus quantity={product.stock_quantity} />

          <div className="mt-8 border-t border-line pt-8">
            <h2 className="sr-only">Description</h2>
            <p className="leading-relaxed whitespace-pre-line text-espresso-soft">
              {product.description}
            </p>
          </div>

          {/* The shopping bag is implemented after P2; the button is shown disabled until then. */}
          <div className="mt-10">
            <button type="button" className="btn-primary w-full sm:w-auto" disabled>
              Add to bag
            </button>
            <p className="mt-3 text-xs text-espresso-soft">Online ordering opens soon.</p>
          </div>

          <dl className="mt-10 grid grid-cols-[auto_1fr] gap-x-8 gap-y-3 border-t border-line pt-8 text-sm">
            <dt className="eyebrow self-center">Category</dt>
            <dd>{product.category.name}</dd>
            {product.collection && (
              <>
                <dt className="eyebrow self-center">Collection</dt>
                <dd>{product.collection.name}</dd>
              </>
            )}
            <dt className="eyebrow self-center">Reference</dt>
            <dd>{product.sku}</dd>
          </dl>
        </section>
      </div>
    </div>
  )
}

function StockStatus({ quantity }: { quantity: number }) {
  if (quantity <= 0) {
    return <p className="mt-3 text-sm font-semibold text-burgundy">Sold out</p>
  }
  if (quantity <= LOW_STOCK_THRESHOLD) {
    return <p className="mt-3 text-sm text-burgundy">Only {quantity} left in stock</p>
  }
  return <p className="mt-3 text-sm text-espresso-soft">In stock</p>
}

function ProductDetailSkeleton() {
  return (
    <div role="status" aria-label="Loading product" className="page-container py-8 sm:py-12">
      <div aria-hidden="true" className="grid animate-pulse gap-10 md:grid-cols-2 lg:gap-16">
        <div className="aspect-[4/5] bg-ivory-deep" />
        <div className="space-y-4 md:pt-4">
          <div className="h-3 w-1/3 bg-ivory-deep" />
          <div className="h-10 w-3/4 bg-ivory-deep" />
          <div className="h-6 w-1/4 bg-ivory-deep" />
          <div className="mt-8 h-24 w-full bg-ivory-deep" />
        </div>
      </div>
    </div>
  )
}
