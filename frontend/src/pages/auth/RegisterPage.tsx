import { useState, type ChangeEvent, type FormEvent } from 'react'
import { Link, Navigate, useLocation } from 'react-router'
import { AuthCard, FormAlert } from '../../components/auth/AuthCard'
import { FormField } from '../../components/ui/FormField'
import { useAuth } from '../../hooks/useAuth'
import {
  hasErrors,
  PASSWORD_MIN_LENGTH,
  toFormFeedback,
  validateRegister,
  type FormErrors,
  type RegisterFormValues,
} from '../../utils/authForms'

type Field = keyof RegisterFormValues

const EMPTY_FORM: RegisterFormValues = {
  first_name: '',
  last_name: '',
  email: '',
  phone_number: '',
  password: '',
  password_confirm: '',
}

export function RegisterPage() {
  const { status, register } = useAuth()
  const state = useLocation().state as { from?: string } | null
  const redirectTo = state?.from ?? '/'

  const [values, setValues] = useState<RegisterFormValues>(EMPTY_FORM)
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

    const clientErrors = validateRegister(values)
    setErrors(clientErrors)
    if (hasErrors(clientErrors)) return

    setSubmitting(true)
    try {
      const phone = values.phone_number.trim()
      await register({
        email: values.email.trim(),
        password: values.password,
        first_name: values.first_name.trim(),
        last_name: values.last_name.trim(),
        ...(phone && { phone_number: phone }),
      })
      // On success the new customer is logged in and <Navigate> redirects.
    } catch (error) {
      const feedback = toFormFeedback<Field>(error)
      setErrors(feedback.fields)
      setFormError(feedback.message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <AuthCard
      eyebrow="Join MAISON NOIR"
      title="Create an account"
      footer={
        <>
          Already have an account?{' '}
          <Link to="/login" state={{ from: redirectTo }} className="font-semibold text-espresso underline-offset-4 hover:text-burgundy hover:underline">
            Sign in
          </Link>
        </>
      }
    >
      <title>Create an account — MAISON NOIR</title>

      {formError && <FormAlert>{formError}</FormAlert>}

      <form noValidate onSubmit={handleSubmit} className="space-y-5">
        <div className="grid gap-5 sm:grid-cols-2">
          <FormField
            label="First name"
            name="first_name"
            autoComplete="given-name"
            value={values.first_name}
            onChange={handleChange}
            error={errors.first_name}
          />
          <FormField
            label="Last name"
            name="last_name"
            autoComplete="family-name"
            value={values.last_name}
            onChange={handleChange}
            error={errors.last_name}
          />
        </div>
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
          label="Phone (optional)"
          name="phone_number"
          type="tel"
          autoComplete="tel"
          value={values.phone_number}
          onChange={handleChange}
          error={errors.phone_number}
        />
        <FormField
          label="Password"
          name="password"
          type="password"
          autoComplete="new-password"
          value={values.password}
          onChange={handleChange}
          error={errors.password}
          hint={`At least ${PASSWORD_MIN_LENGTH} characters, not only numbers.`}
        />
        <FormField
          label="Confirm password"
          name="password_confirm"
          type="password"
          autoComplete="new-password"
          value={values.password_confirm}
          onChange={handleChange}
          error={errors.password_confirm}
        />
        <button type="submit" className="btn-primary w-full" disabled={submitting}>
          {submitting ? 'Creating account…' : 'Create account'}
        </button>
      </form>
    </AuthCard>
  )
}
