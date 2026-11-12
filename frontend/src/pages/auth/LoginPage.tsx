import { useState, type ChangeEvent, type FormEvent } from 'react'
import { Link, Navigate, useLocation } from 'react-router'
import { AuthCard, FormAlert } from '../../components/auth/AuthCard'
import { FormField } from '../../components/ui/FormField'
import { useAuth } from '../../hooks/useAuth'
import {
  hasErrors,
  redirectTarget,
  toFormFeedback,
  validateLogin,
  type FormErrors,
  type LoginFormValues,
} from '../../utils/authForms'

type Field = keyof LoginFormValues

export function LoginPage() {
  const { status, login } = useAuth()
  // After signing in, return to the page that sent the visitor here (else home).
  const redirectTo = redirectTarget(useLocation().state)

  const [values, setValues] = useState<LoginFormValues>({ email: '', password: '' })
  const [errors, setErrors] = useState<FormErrors<Field>>({})
  const [formError, setFormError] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)

  if (status === 'authenticated') {
    return <Navigate to={redirectTo} replace />
  }

  function handleChange(event: ChangeEvent<HTMLInputElement>) {
    const field = event.target.name as Field
    setValues((current) => ({ ...current, [field]: event.target.value }))
    setErrors((current) => ({ ...current, [field]: undefined }))
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setFormError(null)

    const clientErrors = validateLogin(values)
    setErrors(clientErrors)
    if (hasErrors(clientErrors)) return

    setSubmitting(true)
    try {
      await login({ email: values.email.trim(), password: values.password })
      // On success the status becomes "authenticated" and <Navigate> redirects.
    } catch (error) {
      const feedback = toFormFeedback<Field>(error)
      setErrors(feedback.fields)
      setFormError(feedback.message)
      setValues((current) => ({ ...current, password: '' }))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <AuthCard
      eyebrow="Welcome back"
      title="Sign in"
      footer={
        <>
          New to MAISON NOIR?{' '}
          <Link to="/register" state={{ from: redirectTo }} className="font-semibold text-espresso underline-offset-4 hover:text-burgundy hover:underline">
            Create an account
          </Link>
        </>
      }
    >
      <title>Sign in — MAISON NOIR</title>

      {formError && <FormAlert>{formError}</FormAlert>}

      <form noValidate onSubmit={handleSubmit} className="space-y-5">
        <FormField
          label="Email"
          name="email"
          type="email"
          autoComplete="email"
          value={values.email}
          onChange={handleChange}
          error={errors.email}
        />
        <FormField
          label="Password"
          name="password"
          type="password"
          autoComplete="current-password"
          value={values.password}
          onChange={handleChange}
          error={errors.password}
        />
        <button type="submit" className="btn-primary w-full" disabled={submitting}>
          {submitting ? 'Signing in…' : 'Sign in'}
        </button>
      </form>
    </AuthCard>
  )
}
