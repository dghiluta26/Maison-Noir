import type { ReactNode } from 'react'

interface AuthCardProps {
  eyebrow: string
  title: string
  children: ReactNode
  /** Link to the other auth page, shown under the form. */
  footer: ReactNode
}

/** Centred panel shared by the sign-in and registration pages. */
export function AuthCard({ eyebrow, title, children, footer }: AuthCardProps) {
  return (
    <div className="page-container py-12 sm:py-20">
      <div className="mx-auto max-w-md border border-line bg-ivory px-6 py-10 sm:px-10">
        <p className="eyebrow">{eyebrow}</p>
        <h1 className="mt-3 text-4xl">{title}</h1>
        <div className="mt-8">{children}</div>
        <div className="mt-8 border-t border-line pt-6 text-sm text-espresso-soft">{footer}</div>
      </div>
    </div>
  )
}

/** Form-level error (wrong credentials, server unreachable). */
export function FormAlert({ children }: { children: ReactNode }) {
  return (
    <div role="alert" className="mb-6 border border-burgundy/40 bg-burgundy/5 px-4 py-3 text-sm text-burgundy">
      {children}
    </div>
  )
}
