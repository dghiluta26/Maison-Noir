/**
 * Client-side validation and API error mapping for the auth forms.
 * The rules mirror docs/api/auth.md; the backend validates again (and also
 * rejects common passwords or passwords too similar to the name/email).
 */
import { ApiError } from '../services/errors'

/** One message per field, shown under the matching input. */
export type FormErrors<Field extends string> = Partial<Record<Field, string>>

export interface LoginFormValues {
  email: string
  password: string
}

export interface RegisterFormValues {
  first_name: string
  last_name: string
  email: string
  phone_number: string
  password: string
  password_confirm: string
}

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
export const PASSWORD_MIN_LENGTH = 8

function validateEmail(email: string): string | undefined {
  if (!email.trim()) return 'Please enter your email address.'
  if (!EMAIL_PATTERN.test(email.trim())) return 'Please enter a valid email address.'
  return undefined
}

export function validateLogin(values: LoginFormValues): FormErrors<keyof LoginFormValues> {
  const errors: FormErrors<keyof LoginFormValues> = {}
  const email = validateEmail(values.email)
  if (email) errors.email = email
  if (!values.password) errors.password = 'Please enter your password.'
  return errors
}

export function validateRegister(values: RegisterFormValues): FormErrors<keyof RegisterFormValues> {
  const errors: FormErrors<keyof RegisterFormValues> = {}

  if (!values.first_name.trim()) errors.first_name = 'Please enter your first name.'
  else if (values.first_name.trim().length > 150) errors.first_name = 'Use at most 150 characters.'

  if (!values.last_name.trim()) errors.last_name = 'Please enter your last name.'
  else if (values.last_name.trim().length > 150) errors.last_name = 'Use at most 150 characters.'

  const email = validateEmail(values.email)
  if (email) errors.email = email

  if (values.phone_number.trim().length > 20) errors.phone_number = 'Use at most 20 characters.'

  if (!values.password) errors.password = 'Please choose a password.'
  else if (values.password.length < PASSWORD_MIN_LENGTH)
    errors.password = `Use at least ${PASSWORD_MIN_LENGTH} characters.`
  else if (/^\d+$/.test(values.password)) errors.password = 'The password cannot be only numbers.'

  if (!values.password_confirm) errors.password_confirm = 'Please repeat your password.'
  else if (values.password_confirm !== values.password)
    errors.password_confirm = 'The passwords do not match.'

  return errors
}

/** Pages that only make sense for visitors; never redirect back to them after signing in. */
const AUTH_PAGES = ['/login', '/register']

/**
 * Where to go after signing in / registering: the page in `location.state.from`
 * (set by the header link or a protected route), else home. Only same-site paths
 * are accepted, and never the auth pages themselves (that would loop).
 */
export function redirectTarget(state: unknown): string {
  const from =
    state && typeof state === 'object' && 'from' in state && typeof state.from === 'string' ? state.from : ''
  const isSafePath = from.startsWith('/') && !from.startsWith('//')
  const pathname = from.split(/[?#]/)[0]
  return isSafePath && !AUTH_PAGES.includes(pathname) ? from : '/'
}

export function hasErrors(errors: object): boolean {
  return Object.keys(errors).length > 0
}

/**
 * Turns a failed auth request into form feedback:
 * - 400 -> first message of each field (+ non_field_errors as a form message)
 * - 401 -> the API's `detail` (e.g. "Invalid email or password.")
 * - network / other -> a generic message
 */
export function toFormFeedback<Field extends string>(
  error: unknown,
): { fields: FormErrors<Field>; message: string | null } {
  if (error instanceof ApiError) {
    if (error.status === 400) {
      const { non_field_errors: nonField, ...rest } = error.fieldErrors
      const fields = Object.fromEntries(
        Object.entries(rest).map(([field, messages]) => [field, messages[0]]),
      ) as FormErrors<Field>
      return { fields, message: nonField?.[0] ?? null }
    }
    if (error.status === 401) return { fields: {}, message: error.message }
    if (error.status === 0)
      return { fields: {}, message: 'We could not reach the server. Please check your connection and try again.' }
  }
  return { fields: {}, message: 'Something went wrong. Please try again.' }
}
