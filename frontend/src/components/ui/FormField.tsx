import type { InputHTMLAttributes } from 'react'

interface FormFieldProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string
  name: string
  /** Validation message; marks the input invalid for screen readers. */
  error?: string
  /** Helper text shown when there is no error. */
  hint?: string
}

/** Labelled text input with an accessible error / hint message. */
export function FormField({ label, name, error, hint, id = name, className, ...input }: FormFieldProps) {
  const hintId = hint ? `${id}-hint` : undefined
  const errorId = error ? `${id}-error` : undefined

  return (
    <div className={className}>
      <label htmlFor={id} className="eyebrow">
        {label}
      </label>
      <input
        id={id}
        name={name}
        aria-invalid={error ? true : undefined}
        aria-describedby={errorId ?? hintId}
        className={`mt-2 block w-full border bg-ivory px-4 py-3 text-sm text-espresso transition-colors focus:border-espresso ${
          error ? 'border-burgundy' : 'border-line'
        }`}
        {...input}
      />
      {error ? (
        <p id={errorId} className="mt-1.5 text-xs text-burgundy">
          {error}
        </p>
      ) : (
        hint && (
          <p id={hintId} className="mt-1.5 text-xs text-espresso-soft">
            {hint}
          </p>
        )
      )}
    </div>
  )
}
