/**
 * Account service — the ONLY place the UI gets favourites and orders from.
 *
 * PREVIEW: there is no favourites or orders API yet, so this combines mock
 * favourites/orders (src/mocks/account.ts) with REAL products from the live
 * catalogue API. When the endpoints exist, replace the body of
 * getAccountActivity() with authRequest() calls; the page does not change.
 */
import { MOCK_FAVOURITE_SKUS, MOCK_ORDERS } from '../mocks/account'
import type { AccountActivity, Order } from '../types/account'
import type { ProductSummary } from '../types/catalog'
import { getProducts } from './catalogService'

export async function getAccountActivity(): Promise<AccountActivity> {
  // One catalogue request feeds both lists (the default page holds every product).
  const { results } = await getProducts()
  const bySku = new Map(results.map((product) => [product.sku, product]))

  const favourites = MOCK_FAVOURITE_SKUS.flatMap((sku) => bySku.get(sku) ?? [])

  const orders = MOCK_ORDERS.map((mock): Order => {
    const items = mock.items.flatMap(({ sku, quantity }) => {
      const product: ProductSummary | undefined = bySku.get(sku)
      if (!product) return [] // product not in the catalogue response: skip it
      return [{ product, quantity, unit_price: product.price, line_total: money(Number(product.price) * quantity) }]
    })
    const subtotal = items.reduce((sum, item) => sum + Number(item.line_total), 0)
    return {
      number: mock.number,
      placed_at: mock.placed_at,
      status: mock.status,
      delivery_method: mock.delivery_method,
      delivery_cost: mock.delivery_cost,
      items,
      subtotal: money(subtotal),
      total: money(subtotal + Number(mock.delivery_cost)),
    }
  })

  return { favourites, orders }
}

/** Decimal string with two places, like the API ("590.00"). */
function money(amount: number): string {
  return amount.toFixed(2)
}
