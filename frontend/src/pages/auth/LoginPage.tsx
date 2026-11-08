import { Link } from 'react-router'
import { StatusMessage } from '../../components/ui/StatusMessage'

/** Route placeholder — the real login form is built in task 3.2. */
export function LoginPage() {
  return (
    <div className="page-container">
      <title>Sign in — MAISON NOIR</title>
      <StatusMessage
        title="Sign in"
        action={
          <Link to="/products" className="btn-outline">
            Continue shopping
          </Link>
        }
      >
        Customer accounts are coming soon.
      </StatusMessage>
    </div>
  )
}
