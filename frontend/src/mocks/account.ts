/**
 * TEMPORARY mock data for the account page preview (favourites and orders).
 * Only src/services/accountService.ts may import this file; pages never do.
 *
 * Products are referenced by SKU, so the preview shows real catalogue
 * products, images and prices from the live API. Remove this file when the
 * favourites and orders endpoints exist.
 */
import type { OrderStatus } from '../types/account'

export const MOCK_FAVOURITE_SKUS = ['MN-AP-P', 'MN-PD-G', 'MN-SL-D', 'MN-GH-O']

export interface MockOrder {
  number: string
  placed_at: string
  status: OrderStatus
  delivery_method: string
  delivery_cost: string
  items: { sku: string; quantity: number }[]
}

/** Newest first. */
export const MOCK_ORDERS: MockOrder[] = [
  {
    number: 'MN-2026-00131',
    placed_at: '2026-11-11T18:42:00+02:00',
    status: 'paid',
    delivery_method: 'Standard courier (2–3 working days)',
    delivery_cost: '25.00',
    items: [{ sku: 'MN-GH-P', quantity: 1 }],
  },
  {
    number: 'MN-2026-00127',
    placed_at: '2026-11-08T09:15:00+02:00',
    status: 'shipped',
    delivery_method: 'Express courier (next working day)',
    delivery_cost: '40.00',
    items: [
      { sku: 'MN-CC-C', quantity: 2 },
      { sku: 'MN-CC-O', quantity: 1 },
    ],
  },
  {
    number: 'MN-2026-00112',
    placed_at: '2026-10-24T20:05:00+03:00',
    status: 'delivered',
    delivery_method: 'Standard courier (2–3 working days)',
    delivery_cost: '25.00',
    items: [
      { sku: 'MN-MP-P', quantity: 1 },
      { sku: 'MN-NP-C', quantity: 1 },
    ],
  },
]
