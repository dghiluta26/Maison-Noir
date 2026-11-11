import type { MouseEvent } from 'react'
import { Link } from 'react-router'
import heroImage from '../assets/home-parisian-living-room.jpg'
import { ProductCard } from '../components/catalog/ProductCard'
import { ProductGrid, ProductGridSkeleton } from '../components/catalog/ProductGrid'
import { useAsync } from '../hooks/useAsync'
import { getProducts } from '../services/catalogService'
import { isLimitedEdition, pickSignatureSelection } from '../utils/catalog'

const SIGNATURE_COUNT = 4
const COLLECTION_SECTION_ID = 'collection'

/** Smoothly scrolls from the hero to the section right under it (instant for reduced motion). */
function scrollToCollection(event: MouseEvent<HTMLAnchorElement>) {
  event.preventDefault()
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  document
    .getElementById(COLLECTION_SECTION_ID)
    ?.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' })
}

/**
 * Homepage — section order follows the Brand & P1 Project Book, "Homepage structure".
 * Sections still to come: Explore Our Universe (category pages), A Parisian State of Mind
 * and Our Philosophy (editorial content).
 */
export function HomePage() {
  const products = useAsync(getProducts, [])
  const all = products.status === 'success' ? products.data.results : []
  const limitedEditions = all.filter(isLimitedEdition)

  return (
    <>
      <title>MAISON NOIR — The Art of Living Beautifully</title>

      {/* Hero — Parisian living room on the left; a burgundy panel slides in from the right */}
      <section className="relative h-dvh min-h-[36rem] overflow-hidden bg-burgundy">
        {/* Picture, framed on the sofa and the Eiffel Tower view:
            top 55% of the screen on phones, the left 62% from md up. */}
        <img
          src={heroImage}
          alt="A Parisian apartment at sunset: a marble fireplace, a cream sofa and a view of the Eiffel Tower"
          fetchPriority="high"
          className="absolute inset-x-0 top-0 h-[55%] w-full object-cover object-[75%_center] md:inset-y-0 md:right-auto md:h-full md:w-[62%] md:object-right"
        />

        {/* Burgundy panel: lower part of the screen on phones, right side from md up.
            Its edge fades into the picture. */}
        <div className="absolute inset-x-0 bottom-0 flex h-[58%] items-end bg-linear-to-t from-burgundy from-85% to-burgundy/0 motion-safe:animate-slide-in-right md:inset-x-auto md:inset-y-0 md:right-0 md:h-full md:w-[54%] md:items-center lg:w-[46%] md:bg-linear-to-l md:from-80%">
          {/* From md up, the left padding (a % of the panel width) keeps the text on the
              solid burgundy, clear of the faded edge, at every screen width. */}
          <div className="w-full px-6 pb-12 sm:px-10 md:pr-10 md:pb-0 md:pl-[23%] lg:pr-16 lg:pl-[30%]">
            <p className="text-sm font-semibold tracking-brand text-champagne uppercase motion-safe:animate-fade-up motion-safe:[animation-delay:700ms] sm:text-base">
              MAISON NOIR
            </p>
            <h1 className="mt-5 text-[2rem] leading-[1.08] text-ivory motion-safe:animate-fade-up motion-safe:[animation-delay:900ms] sm:text-5xl lg:text-6xl">
              The Art of Living Beautifully
            </h1>
            <p className="mt-6 max-w-sm text-sm leading-relaxed text-taupe motion-safe:animate-fade-up motion-safe:[animation-delay:1100ms]">
              Inspired by Parisian interiors and the art of niche perfumery, Maison Noir brings
              together personal fragrances, scented candles, reed diffusers, and a small collection
              of sculptural objects.
            </p>
            <a
              href={`#${COLLECTION_SECTION_ID}`}
              onClick={scrollToCollection}
              className="btn mt-8 bg-ivory whitespace-nowrap text-espresso hover:bg-champagne md:px-5 lg:px-7 motion-safe:animate-fade-up motion-safe:[animation-delay:1300ms] sm:mt-10"
            >
              Discover the Collection
            </a>
          </div>
        </div>
      </section>

      {/* Signature Selection — target of the hero's "Discover the Collection" button.
          scroll-mt leaves room for the header that appears on scroll. */}
      <section
        id={COLLECTION_SECTION_ID}
        className="page-container scroll-mt-16 py-16 sm:scroll-mt-20 sm:py-24"
      >
        <div className="mb-10 flex items-end justify-between gap-4">
          <div>
            <p className="eyebrow">Curated for you</p>
            <h2 className="mt-3 text-3xl sm:text-4xl">Signature Selection</h2>
          </div>
          <Link to="/products" className="eyebrow border-b border-espresso pb-1 hover:text-burgundy">
            View all
          </Link>
        </div>

        {products.status === 'loading' && <ProductGridSkeleton count={SIGNATURE_COUNT} />}
        {products.status === 'success' && (
          <ProductGrid products={pickSignatureSelection(all, SIGNATURE_COUNT)} />
        )}
        {/* On error the section is simply empty; the Shop page shows the full error state. */}
      </section>

      {/* Limited Editions */}
      {limitedEditions.length > 0 && (
        <section className="bg-sand py-16 sm:py-24">
          <div className="page-container grid items-center gap-12 lg:grid-cols-[1fr_2fr]">
            <div>
              <p className="text-xs font-semibold tracking-[0.18em] text-burgundy uppercase">
                Strictly limited
              </p>
              <h2 className="mt-3 text-3xl sm:text-4xl">Limited Editions</h2>
              <p className="mt-4 max-w-sm text-sm leading-relaxed text-espresso-soft">
                Only two MAISON NOIR collections are offered as gift sets, each produced in very
                small numbers.
              </p>
            </div>
            <ul className="grid grid-cols-2 gap-x-4 gap-y-10 sm:gap-x-6">
              {limitedEditions.map((product) => (
                <li key={product.id}>
                  <ProductCard product={product} />
                </li>
              ))}
            </ul>
          </div>
        </section>
      )}
    </>
  )
}
