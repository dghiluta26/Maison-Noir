/**
 * Catalogue service — the ONLY place the UI gets catalogue data from.
 *
 * TEMPORARY: backed by mock data until the catalogue API (task 2.4) exists.
 * In task 2.5 the bodies of these functions are replaced with HTTP calls to
 *   GET /api/categories/
 *   GET /api/products/
 *   GET /api/products/{slug}/
 * Their signatures stay the same, so pages and components do not change.
 */
import { mockCategories, mockProducts } from '../mocks/catalog'
import type { Category, Paginated, ProductDetail, ProductSummary } from '../types/catalog'
import { ApiError } from './errors'

/** Simulated network latency so loading states are visible during development. */
const MOCK_DELAY_MS = 300

function delay<T>(value: T): Promise<T> {
  return new Promise((resolve) => setTimeout(() => resolve(value), MOCK_DELAY_MS))
}

function toSummary({ description: _d, images: _i, ...summary }: ProductDetail): ProductSummary {
  return summary
}

export async function getCategories(): Promise<Category[]> {
  return delay(mockCategories)
}

export async function getProducts(): Promise<Paginated<ProductSummary>> {
  const results = mockProducts.map(toSummary)
  return delay({ count: results.length, next: null, previous: null, results })
}

export async function getProduct(slug: string): Promise<ProductDetail> {
  const product = mockProducts.find((p) => p.slug === slug)
  if (!product) {
    await delay(null)
    throw new ApiError('Product not found.', 404)
  }
  return delay(product)
}
