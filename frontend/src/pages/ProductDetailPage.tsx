import { Fragment, useState, type ReactNode } from 'react'
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
          <li>
            <Link to={catalogueLink('category', product.category.slug)} className="hover:text-burgundy">
              {product.category.name}
            </Link>
          </li>
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
          {product.tagline && (
            <p className="mt-3 font-serif text-xl text-espresso-soft italic">{product.tagline}</p>
          )}
          <p className="mt-5 text-xl font-semibold">
            {formatPrice(product.price)}
            {product.size && <span className="ml-3 text-sm font-normal text-espresso-soft">{product.size}</span>}
          </p>

          <StockStatus quantity={product.stock_quantity} />

          {product.description && (
            <div className="mt-8 border-t border-line pt-8">
              <h2 className="sr-only">Description</h2>
              <p className="leading-relaxed whitespace-pre-line text-espresso-soft">
                {product.description}
              </p>
            </div>
          )}

          <ScentNotes product={product} />

          {product.ritual && (
            <div className="mt-8">
              <h2 className="eyebrow">The ritual</h2>
              <p className="mt-3 text-sm leading-relaxed whitespace-pre-line text-espresso-soft">
                {product.ritual}
              </p>
            </div>
          )}

          {/* The shopping bag is implemented after P2; the button is shown disabled until then. */}
          <div className="mt-10">
            <button type="button" className="btn-primary w-full sm:w-auto" disabled>
              Add to bag
            </button>
            <p className="mt-3 text-xs text-espresso-soft">Online ordering opens soon.</p>
          </div>

          <ProductFacts product={product} />
        </section>
      </div>
    </div>
  )
}

/** Shop page filtered by one category or collection. */
function catalogueLink(filter: 'category' | 'collection', slug: string): string {
  return `/products?${new URLSearchParams({ [filter]: slug })}`
}

/** Top, heart and base notes; hidden when the product has none (e.g. design objects). */
function ScentNotes({ product }: { product: ProductDetail }) {
  const notes = [
    { label: 'Top', value: product.notes_top },
    { label: 'Heart', value: product.notes_heart },
    { label: 'Base', value: product.notes_base },
  ].filter((note) => note.value)

  if (notes.length === 0) return null

  return (
    <div className="mt-8">
      <h2 className="eyebrow">Olfactory notes</h2>
      <dl className="mt-3 divide-y divide-line border-y border-line text-sm">
        {notes.map(({ label, value }) => (
          <div key={label} className="grid grid-cols-[5rem_1fr] gap-4 py-3">
            <dt className="font-semibold">{label}</dt>
            <dd className="text-espresso-soft">{value}</dd>
          </div>
        ))}
      </dl>
    </div>
  )
}

/** Reference table at the bottom of the product page; empty details are skipped. */
function ProductFacts({ product }: { product: ProductDetail }) {
  const linkClass = 'underline-offset-4 hover:text-burgundy hover:underline'
  const facts: { label: string; value: ReactNode }[] = [
    {
      label: 'Category',
      value: (
        <Link to={catalogueLink('category', product.category.slug)} className={linkClass}>
          {product.category.name}
        </Link>
      ),
    },
  ]
  if (product.collection) {
    facts.push({
      label: 'Collection',
      value: (
        <Link to={catalogueLink('collection', product.collection.slug)} className={linkClass}>
          {product.collection.name}
        </Link>
      ),
    })
  }
  const optional: [string, string][] = [
    ['Size', product.size],
    ['Duration', product.burn_time],
    ['Includes', product.includes],
    ['Materials', product.materials],
    ['Edition', product.edition],
  ]
  for (const [label, value] of optional) {
    if (value) facts.push({ label, value: <span className="whitespace-pre-line">{value}</span> })
  }
  facts.push({ label: 'Reference', value: product.sku })

  return (
    <dl className="mt-10 grid grid-cols-[auto_1fr] gap-x-8 gap-y-3 border-t border-line pt-8 text-sm">
      {facts.map(({ label, value }) => (
        <Fragment key={label}>
          <dt className="eyebrow pt-0.5">{label}</dt>
          <dd>{value}</dd>
        </Fragment>
      ))}
    </dl>
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
