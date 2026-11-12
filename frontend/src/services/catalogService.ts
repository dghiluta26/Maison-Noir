/**
 * Catalogue service — the ONLY place the UI gets catalogue data from.
 *
 * Backed by the live Django REST API (see docs/api/catalogue.md):
 *   GET /api/categories/        -> Category[]
 *   GET /api/products/          -> Paginated<ProductSummary>
 *   GET /api/products/{slug}/   -> ProductDetail (404 if unknown or inactive)
 * Failures are raised as ApiError (see ./errors).
 */
import type { Category, Paginated, ProductDetail, ProductSummary } from '../types/catalog'
import { apiGet } from './apiClient'

export async function getCategories(): Promise<Category[]> {
  return apiGet<Category[]>('/categories/')
}

export async function getProducts(): Promise<Paginated<ProductSummary>> {
  return apiGet<Paginated<ProductSummary>>('/products/')
}

export async function getProduct(slug: string): Promise<ProductDetail> {
  return apiGet<ProductDetail>(`/products/${encodeURIComponent(slug)}/`)
}
