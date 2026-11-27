/**
 * Catalogue types.
 *
 * These interfaces mirror the JSON returned by the Django REST API
 * (snake_case field names, exactly as DRF serializes them), so the
 * service layer can return API data without renaming fields.
 *
 * Contract: docs/api/catalogue.md.
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

/** Category as listed by GET /api/categories/. */
export interface CategoryListItem extends Category {
  description: string
}

/** Collection as listed by GET /api/collections/. Empty texts are "". */
export interface CollectionListItem extends Collection {
  description: string
  tagline: string
  story: string
  /** Absolute URL of the collection picture, or null. */
  image: string | null
  launch_year: number | null
}

/** Query parameters accepted by GET /api/products/. Empty values are not sent. */
export interface ProductQuery {
  search?: string
  /** Category slug. */
  category?: string
  /** Collection slug. */
  collection?: string
  /** 1-based page number. */
  page?: number
  page_size?: number
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

/**
 * Full product as shown on its detail page (GET /api/products/{slug}/).
 * The optional details are "" when they do not apply to the product.
 */
export interface ProductDetail extends ProductSummary {
  description: string
  tagline: string
  size: string
  burn_time: string
  includes: string
  notes_top: string
  notes_heart: string
  notes_base: string
  materials: string
  edition: string
  ritual: string
  images: ProductImage[]
}

/** DRF PageNumberPagination envelope. */
export interface Paginated<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}
