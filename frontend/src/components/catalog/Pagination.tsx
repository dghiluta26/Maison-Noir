import { Link, type To } from 'react-router'

interface PaginationProps {
  /** Current page, 1-based. */
  page: number
  totalPages: number
  /** Link target for a given page (keeps the other filters in the URL). */
  pageLink: (page: number) => To
}

/** Neighbours shown on each side of the current page before an ellipsis is used. */
const SIBLINGS = 1

/** Page numbers to show, with null where pages are skipped: 1 … 4 5 6 … 10. */
function visiblePages(page: number, totalPages: number): (number | null)[] {
  const pages: (number | null)[] = []
  for (let n = 1; n <= totalPages; n += 1) {
    const shown = n === 1 || n === totalPages || Math.abs(n - page) <= SIBLINGS
    if (shown) pages.push(n)
    else if (pages.at(-1) !== null) pages.push(null)
  }
  return pages
}

const itemClass =
  'inline-flex h-10 min-w-10 items-center justify-center border px-3 text-xs font-semibold tracking-[0.14em] uppercase transition-colors'

/** Previous / numbered / next links for a paginated list. Renders nothing for a single page. */
export function Pagination({ page, totalPages, pageLink }: PaginationProps) {
  if (totalPages <= 1) return null

  return (
    <nav aria-label="Pagination" className="mt-16 flex justify-center">
      <ul className="flex flex-wrap items-center justify-center gap-2">
        <li>
          {page > 1 ? (
            <Link to={pageLink(page - 1)} className={`${itemClass} border-line hover:border-espresso`}>
              Previous
            </Link>
          ) : (
            <span aria-disabled="true" className={`${itemClass} border-line text-espresso-soft opacity-50`}>
              Previous
            </span>
          )}
        </li>

        {visiblePages(page, totalPages).map((n, index) =>
          n === null ? (
            <li key={`gap-${index}`} aria-hidden="true" className="px-1 text-espresso-soft">
              …
            </li>
          ) : (
            <li key={n}>
              <Link
                to={pageLink(n)}
                aria-label={`Page ${n}`}
                aria-current={n === page ? 'page' : undefined}
                className={`${itemClass} ${
                  n === page ? 'border-espresso bg-espresso text-ivory' : 'border-line hover:border-espresso'
                }`}
              >
                {n}
              </Link>
            </li>
          ),
        )}

        <li>
          {page < totalPages ? (
            <Link to={pageLink(page + 1)} className={`${itemClass} border-line hover:border-espresso`}>
              Next
            </Link>
          ) : (
            <span aria-disabled="true" className={`${itemClass} border-line text-espresso-soft opacity-50`}>
              Next
            </span>
          )}
        </li>
      </ul>
    </nav>
  )
}
