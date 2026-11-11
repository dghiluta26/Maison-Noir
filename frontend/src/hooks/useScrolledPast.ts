import { useEffect, useState } from 'react'

/** True once the page has been scrolled more than `threshold` pixels down. */
export function useScrolledPast(threshold: number): boolean {
  const [scrolledPast, setScrolledPast] = useState(false)

  useEffect(() => {
    const update = () => setScrolledPast(window.scrollY > threshold)
    update() // correct value after a reload or restored scroll position
    window.addEventListener('scroll', update, { passive: true })
    return () => window.removeEventListener('scroll', update)
  }, [threshold])

  return scrolledPast
}
