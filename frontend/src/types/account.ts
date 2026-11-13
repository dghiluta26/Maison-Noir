/**
 * Account area types (favourites and order history).
 *
 * PREVIEW: there is no orders or favourites API yet. These shapes are a
 * frontend draft; align them with the backend contract when it exists.
 */
import type { ProductSummary } from './catalog'

/** Order lifecycle from the project spec (A9): New → Paid → Shipped → Delivered, or Cancelled. */
export type OrderStatus = 'new' | 'paid' | 'shipped' | 'delivered' | 'cancelled'

export interface OrderItem {
  product: ProductSummary
  quantity: number
  /** Price in lei at the time of the order, as a decimal string ("590.00"). */
  unit_price: string
  line_total: string
}

export interface Order {
  /** Human-readable order number, e.g. "MN-2026-00112". */
  number: string
  /** ISO 8601 date-time. */
  placed_at: string
  status: OrderStatus
  delivery_method: string
  delivery_cost: string
  items: OrderItem[]
  subtotal: string
  total: string
}

/** Everything the account page shows besides the profile itself. */
export interface AccountActivity {
  favourites: ProductSummary[]
  orders: Order[]
}
