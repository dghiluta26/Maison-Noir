import type { ProductImage } from '../../types/catalog'

interface ProductImageFrameProps {
  image: ProductImage | null
  /** Used as alt text when the image has none, and shown on the placeholder. */
  productName: string
  className?: string
  /** Load eagerly for above-the-fold images (e.g. the product-detail hero). */
  eager?: boolean
}

/**
 * Product image in a fixed 4:5 frame, so grids stay aligned whatever the
 * source dimensions. Shows a branded placeholder when there is no image.
 */
export function ProductImageFrame({ image, productName, className = '', eager = false }: ProductImageFrameProps) {
  return (
    <div className={`relative aspect-[4/5] overflow-hidden bg-ivory-deep ${className}`}>
      {image ? (
        <img
          src={image.image}
          alt={image.alt_text || productName}
          loading={eager ? 'eager' : 'lazy'}
          className="h-full w-full object-cover"
        />
      ) : (
        <div
          role="img"
          aria-label={`${productName} — image coming soon`}
          className="flex h-full w-full flex-col items-center justify-center gap-3 bg-gradient-to-b from-ivory to-ivory-deep"
        >
          <span aria-hidden="true" className="font-serif text-5xl text-champagne">
            MN
          </span>
          <span aria-hidden="true" className="h-px w-10 bg-champagne/60" />
        </div>
      )}
    </div>
  )
}
