/**
 * Catalogue types.
 *
 * These interfaces mirror the JSON returned by the Django REST API
 * (snake_case field names, exactly as DRF serializes them), so the
 * service layer can return API data without renaming fields.
 *
 * Draft contract — to be confirmed with the backend in tasks 2.2 / 2.4.
 */

export interface Category {
  id: number
  name: string
  slug: string
}

export interface Collection {
  id: number
  name: string
  slug: string
}

export interface ProductImage {
  id: number
  /** Absolute URL of the image file. */
  image: string
  alt_text: string
  is_primary: boolean
}

/** Product as shown in the catalogue grid (GET /api/products/). */
export interface ProductSummary {
  id: number
  /** Catalogue code, e.g. "MN-AH-P". */
  sku: string
  name: string
  slug: string
  /** Price in lei. DRF serializes DecimalField as a string, e.g. "590.00", to avoid float rounding. */
  price: string
  category: Category
  collection: Collection | null
  primary_image: ProductImage | null
  in_stock: boolean
  /** Needed in the grid for the low-stock labels required by the Brand Book. */
  stock_quantity: number
}

/** Full product as shown on its detail page (GET /api/products/{slug}/). */
export interface ProductDetail extends ProductSummary {
  description: string
  images: ProductImage[]
}

/** DRF PageNumberPagination envelope. */
export interface Paginated<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}
