import type { FormEvent } from 'react'
import { Link, useSearchParams } from 'react-router'
import { Pagination } from '../components/catalog/Pagination'
import { ProductGrid, ProductGridSkeleton } from '../components/catalog/ProductGrid'
import { StatusMessage } from '../components/ui/StatusMessage'
import { useAsync } from '../hooks/useAsync'
import { CATALOGUE_PAGE_SIZE, getCategories, getCollections, getProducts } from '../services/catalogService'
import { isNotFound } from '../services/errors'

/** Reads ?page= from the URL; anything that is not a whole number >= 1 means page 1. */
function parsePage(value: string | null): number {
  const page = Number(value)
  return Number.isInteger(page) && page >= 1 ? page : 1
}

/**
 * Shop page. All state lives in the URL, so results can be shared, refreshed
 * and navigated with Back / Forward:
 *   ?search=  ?category=<slug>  ?collection=<slug>  ?page=
 */
export function CataloguePage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const search = (searchParams.get('search') ?? '').trim()
  const category = searchParams.get('category') ?? ''
  const collection = searchParams.get('collection') ?? ''
  const page = parsePage(searchParams.get('page'))

  const products = useAsync(
    () => getProducts({ search, category, collection, page }),
    [search, category, collection, page],
  )
  const selection = useSelectionInfo(category, collection)

  /** URL for one page of the current results (page 1 is left out of the URL). */
  function pageLink(target: number) {
    const params = new URLSearchParams(searchParams)
    if (target > 1) params.set('page', String(target))
    else params.delete('page')
    return { search: params.toString() }
  }

  /** Changes or clears the search term and goes back to the first page. */
  function applySearch(term: string) {
    const params = new URLSearchParams(searchParams)
    if (term) params.set('search', term)
    else params.delete('search')
    params.delete('page')
    setSearchParams(params)
  }

  function handleSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const term = new FormData(event.currentTarget).get('search')
    applySearch(typeof term === 'string' ? term.trim() : '')
  }

  const totalPages = products.status === 'success' ? Math.ceil(products.data.count / CATALOGUE_PAGE_SIZE) : 0
  const title = search ? `Results for “${search}”` : (selection?.name ?? 'All products')

  return (
    <div className="page-container py-12 sm:py-16">
      <title>{`${selection?.name ?? 'Shop'} — MAISON NOIR`}</title>

      <header className="mb-10 border-b border-line pb-8 sm:mb-14">
        <p className="eyebrow">{selection?.kind ?? 'The collection'}</p>
        <h1 className="mt-3 text-4xl break-words sm:text-5xl">{title}</h1>
        {selection?.description && !search && (
          <p className="mt-3 max-w-2xl text-sm leading-relaxed text-espresso-soft">{selection.description}</p>
        )}

        <div className="mt-8 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <form role="search" onSubmit={handleSearch} className="flex w-full max-w-md">
            <label htmlFor="catalogue-search" className="sr-only">
              Search products
            </label>
            <input
              // Re-created when the URL changes, so Back / Forward update the box.
              key={search}
              id="catalogue-search"
              name="search"
              type="search"
              defaultValue={search}
              placeholder="Search by name, scent or collection"
              autoComplete="off"
              className="min-w-0 flex-1 border border-r-0 border-line bg-ivory px-4 py-3 text-sm text-espresso placeholder:text-espresso-soft focus:border-espresso"
            />
            <button type="submit" className="btn-primary px-5">
              Search
            </button>
          </form>

          {products.status === 'success' && (
            <p className="text-sm text-espresso-soft" aria-live="polite">
              {products.data.count} {products.data.count === 1 ? 'product' : 'products'}
              {totalPages > 1 && ` · Page ${page} of ${totalPages}`}
            </p>
          )}
        </div>

        {(search || category || collection) && (
          <p className="mt-4 flex flex-wrap gap-x-6 gap-y-2 text-xs">
            {search && (
              <button type="button" onClick={() => applySearch('')} className="eyebrow text-burgundy hover:underline">
                Clear search
              </button>
            )}
            {(category || collection) && (
              <Link to="/products" className="eyebrow text-burgundy hover:underline">
                View all products
              </Link>
            )}
          </p>
        )}
      </header>

      {products.status === 'loading' && <ProductGridSkeleton />}

      {products.status === 'error' &&
        (isNotFound(products.error) ? (
          // DRF answers 404 for a page number past the last page.
          <StatusMessage
            title="This page does not exist"
            action={
              <Link to={pageLink(1)} className="btn-outline">
                Go to the first page
              </Link>
            }
          >
            There are fewer products than this page number suggests.
          </StatusMessage>
        ) : (
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
        ))}

      {products.status === 'success' &&
        (products.data.results.length > 0 ? (
          <>
            <ProductGrid products={products.data.results} />
            <Pagination page={page} totalPages={totalPages} pageLink={pageLink} />
          </>
        ) : search ? (
          <StatusMessage
            title="No products found"
            action={
              <button type="button" className="btn-outline" onClick={() => applySearch('')}>
                Clear search
              </button>
            }
          >
            Nothing matches “{search}”. Try another name, scent or collection.
          </StatusMessage>
        ) : (
          <StatusMessage
            title="No products here yet"
            action={
              <Link to="/products" className="btn-outline">
                View all products
              </Link>
            }
          >
            This selection is being prepared. Please come back soon.
          </StatusMessage>
        ))}
    </div>
  )
}

interface SelectionInfo {
  kind: 'Category' | 'Collection'
  name: string
  description: string
}

/**
 * Name and description of the category or collection in the URL, for the page
 * heading. Null while loading, for an unknown slug, or when nothing is selected
 * (the page then falls back to "All products").
 */
function useSelectionInfo(category: string, collection: string): SelectionInfo | null {
  const lists = useAsync(
    () => (category || collection ? Promise.all([getCategories(), getCollections()]) : Promise.resolve(null)),
    [category, collection],
  )
  if (lists.status !== 'success' || lists.data === null) return null

  const [categories, collections] = lists.data
  if (collection) {
    const match = collections.find((item) => item.slug === collection)
    return match ? { kind: 'Collection', name: match.name, description: match.tagline || match.description } : null
  }
  const match = categories.find((item) => item.slug === category)
  return match ? { kind: 'Category', name: match.name, description: match.description } : null
}
