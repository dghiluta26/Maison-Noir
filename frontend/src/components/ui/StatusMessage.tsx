import type { ReactNode } from 'react'

interface StatusMessageProps {
  title: string
  children?: ReactNode
  /** Optional call to action, e.g. a retry button or a link. */
  action?: ReactNode
  /** Use "alert" for errors so screen readers announce them immediately. */
  role?: 'status' | 'alert'
}

/** Centred message used for empty, error and not-found states. */
export function StatusMessage({ title, children, action, role = 'status' }: StatusMessageProps) {
  return (
    <div role={role} className="mx-auto max-w-md py-20 text-center">
      <p className="font-serif text-3xl">{title}</p>
      {children && <div className="mt-3 text-sm leading-relaxed text-espresso-soft">{children}</div>}
      {action && <div className="mt-8">{action}</div>}
    </div>
  )
}
