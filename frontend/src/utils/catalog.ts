import type { ProductSummary } from '../types/catalog'

/** Category whose products are labelled "Limited Edition" (Brand Book: two gift sets). */
export const LIMITED_EDITION_CATEGORY_SLUG = 'limited-gift-sets'

/** Stock at or below this level shows an "Only N left" label. */
export const LOW_STOCK_THRESHOLD = 3

export function isLimitedEdition(product: ProductSummary): boolean {
  return product.category.slug === LIMITED_EDITION_CATEGORY_SLUG
}

export function isLowStock(product: ProductSummary): boolean {
  return product.in_stock && product.stock_quantity <= LOW_STOCK_THRESHOLD
}

/**
 * Homepage "Signature Selection" (Brand Book: 4-8 representative products).
 * Takes the first product of each category so the selection spans the range;
 * gift sets are left out because they have their own "Limited Editions" section.
 * Can later be replaced by a backend "featured" flag without changing the page.
 */
export function pickSignatureSelection(products: ProductSummary[], limit = 4): ProductSummary[] {
  const seen = new Set<number>()
  const selection: ProductSummary[] = []
  for (const product of products) {
    if (!isLimitedEdition(product) && !seen.has(product.category.id)) {
      seen.add(product.category.id)
      selection.push(product)
    }
    if (selection.length === limit) break
  }
  return selection
}
