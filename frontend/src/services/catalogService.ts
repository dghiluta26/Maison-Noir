/**
 * Catalogue service — the ONLY place the UI gets catalogue data from.
 *
 * Backed by the live Django REST API (see docs/api/catalogue.md):
 *   GET /api/categories/        -> CategoryListItem[]
 *   GET /api/collections/       -> CollectionListItem[]
 *   GET /api/products/          -> Paginated<ProductSummary>
 *                                  ?search= &category= &collection= &page= &page_size=
 *   GET /api/products/{slug}/   -> ProductDetail (404 if unknown or inactive)
 * Failures are raised as ApiError (see ./errors).
 */
import type {
  CategoryListItem,
  CollectionListItem,
  Paginated,
  ProductDetail,
  ProductQuery,
  ProductSummary,
} from '../types/catalog'
import { apiGet } from './apiClient'

/** Products per catalogue page (P3 rule: at most 24). Sent explicitly on every list request. */
export const CATALOGUE_PAGE_SIZE = 24

export async function getCategories(): Promise<CategoryListItem[]> {
  return apiGet<CategoryListItem[]>('/categories/')
}

export async function getCollections(): Promise<CollectionListItem[]> {
  return apiGet<CollectionListItem[]>('/collections/')
}

/** One page of products. */
export async function getProducts(query: ProductQuery = {}): Promise<Paginated<ProductSummary>> {
  return apiGet<Paginated<ProductSummary>>(`/products/${toQueryString({ page_size: CATALOGUE_PAGE_SIZE, ...query })}`)
}

/**
 * Every product matching the filters, following the pages one after another.
 * For small sets only (homepage selection, account preview); the shop page
 * itself loads one page at a time.
 */
export async function getAllProducts(
  query: Omit<ProductQuery, 'page' | 'page_size'> = {},
): Promise<ProductSummary[]> {
  const products: ProductSummary[] = []
  for (let page = 1; ; page += 1) {
    const { results, next } = await getProducts({ ...query, page })
    products.push(...results)
    if (!next) return products
  }
}

export async function getProduct(slug: string): Promise<ProductDetail> {
  return apiGet<ProductDetail>(`/products/${encodeURIComponent(slug)}/`)
}

/** "?a=1&b=x" from the non-empty values, or "" when there are none. */
function toQueryString(query: ProductQuery): string {
  const params = new URLSearchParams()
  for (const [key, value] of Object.entries(query)) {
    if (value === undefined || value === '') continue
    params.set(key, String(value))
  }
  const text = params.toString()
  return text ? `?${text}` : ''
}
