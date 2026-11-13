import { Link } from 'react-router'
import type { Order, OrderStatus } from '../../types/account'
import { formatPrice } from '../../utils/format'
import { ProductImageFrame } from '../catalog/ProductImageFrame'

const STATUS: Record<OrderStatus, { label: string; className: string }> = {
  new: { label: 'New', className: 'border border-taupe text-espresso-soft' },
  paid: { label: 'Paid', className: 'border border-champagne bg-champagne/15 text-espresso' },
  shipped: { label: 'Shipped', className: 'bg-espresso text-ivory' },
  delivered: { label: 'Delivered', className: 'bg-burgundy text-ivory' },
  cancelled: { label: 'Cancelled', className: 'border border-line text-espresso-soft' },
}

const orderDate = new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'long', year: 'numeric' })

export function OrderStatusBadge({ status }: { status: OrderStatus }) {
  const { label, className } = STATUS[status]
  return (
    <span className={`inline-block px-2.5 py-1 text-[0.65rem] font-semibold tracking-[0.16em] uppercase ${className}`}>
      {label}
    </span>
  )
}

/** Orders newest first; each one expands to show its items and totals. */
export function OrderHistory({ orders }: { orders: Order[] }) {
  if (orders.length === 0) {
    return (
      <div className="border border-line bg-ivory px-6 py-12 text-center">
        <p className="font-serif text-2xl">No orders yet</p>
        <p className="mt-2 text-sm text-espresso-soft">Your orders will appear here once you have placed one.</p>
        <Link to="/products" className="btn-primary mt-8">
          Discover the collections
        </Link>
      </div>
    )
  }

  return (
    <ul className="space-y-4">
      {orders.map((order, index) => (
        <li key={order.number}>
          <OrderCard order={order} defaultOpen={index === 0} />
        </li>
      ))}
    </ul>
  )
}

function OrderCard({ order, defaultOpen }: { order: Order; defaultOpen: boolean }) {
  const itemCount = order.items.reduce((sum, item) => sum + item.quantity, 0)

  return (
    <details open={defaultOpen} className="group border border-line bg-ivory">
      <summary className="flex cursor-pointer list-none flex-wrap items-center gap-x-6 gap-y-3 px-5 py-4 sm:px-6 [&::-webkit-details-marker]:hidden">
        <div className="min-w-0 flex-1">
          <p className="eyebrow">Order</p>
          <p className="mt-1 font-serif text-xl">{order.number}</p>
        </div>
        <div className="hidden sm:block">
          <p className="eyebrow">Placed</p>
          <p className="mt-1 text-sm">{orderDate.format(new Date(order.placed_at))}</p>
        </div>
        <OrderStatusBadge status={order.status} />
        <p className="w-24 text-right text-sm font-semibold">{formatPrice(order.total)}</p>
        <span aria-hidden="true" className="text-champagne transition-transform duration-200 group-open:rotate-180">
          ⌄
        </span>
      </summary>

      <div className="border-t border-line px-5 py-5 sm:px-6">
        <p className="text-xs text-espresso-soft sm:hidden">Placed {orderDate.format(new Date(order.placed_at))}</p>

        <ul className="divide-y divide-line">
          {order.items.map((item) => (
            <li key={item.product.sku} className="flex items-center gap-4 py-4 first:pt-0">
              <Link to={`/products/${item.product.slug}`} className="w-16 shrink-0 sm:w-20">
                <ProductImageFrame image={item.product.primary_image} productName={item.product.name} />
              </Link>
              <div className="min-w-0 flex-1">
                <Link
                  to={`/products/${item.product.slug}`}
                  className="font-serif text-lg leading-snug hover:text-burgundy"
                >
                  {item.product.name}
                </Link>
                <p className="mt-1 text-xs text-espresso-soft">
                  {item.quantity} × {formatPrice(item.unit_price)}
                </p>
              </div>
              <p className="text-sm font-semibold">{formatPrice(item.line_total)}</p>
            </li>
          ))}
        </ul>

        <dl className="mt-2 space-y-2 border-t border-line pt-4 text-sm">
          <div className="flex justify-between gap-4">
            <dt className="text-espresso-soft">
              Subtotal ({itemCount} {itemCount === 1 ? 'item' : 'items'})
            </dt>
            <dd>{formatPrice(order.subtotal)}</dd>
          </div>
          <div className="flex justify-between gap-4">
            <dt className="text-espresso-soft">{order.delivery_method}</dt>
            <dd>{formatPrice(order.delivery_cost)}</dd>
          </div>
          <div className="flex justify-between gap-4 border-t border-line pt-3 font-semibold">
            <dt>Total</dt>
            <dd>{formatPrice(order.total)}</dd>
          </div>
        </dl>
      </div>
    </details>
  )
}
