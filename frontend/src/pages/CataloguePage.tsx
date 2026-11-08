import { ProductGrid, ProductGridSkeleton } from '../components/catalog/ProductGrid'
import { StatusMessage } from '../components/ui/StatusMessage'
import { useAsync } from '../hooks/useAsync'
import { getProducts } from '../services/catalogService'

export function CataloguePage() {
  const products = useAsync(getProducts, [])

  return (
    <div className="page-container py-12 sm:py-16">
      <title>Shop — MAISON NOIR</title>

      <header className="mb-10 border-b border-line pb-8 sm:mb-14">
        <p className="eyebrow">The collection</p>
        <h1 className="mt-3 text-4xl sm:text-5xl">All products</h1>
        {products.status === 'success' && (
          <p className="mt-3 text-sm text-espresso-soft">
            {products.data.count} {products.data.count === 1 ? 'product' : 'products'}
          </p>
        )}
      </header>

      {products.status === 'loading' && <ProductGridSkeleton />}

      {products.status === 'error' && (
        <StatusMessage
          role="alert"
          title="We couldn't load the collection"
          action={
            <button type="button" className="btn-outline" onClick={products.retry}>
              Try again
            </button>
          }
        >
          Please check your connection and try again.
        </StatusMessage>
      )}

      {products.status === 'success' &&
        (products.data.results.length > 0 ? (
          <ProductGrid products={products.data.results} />
        ) : (
          <StatusMessage title="No products yet">
            The collection is being prepared. Please come back soon.
          </StatusMessage>
        ))}
    </div>
  )
}
