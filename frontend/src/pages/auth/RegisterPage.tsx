import { Link } from 'react-router'
import { StatusMessage } from '../../components/ui/StatusMessage'

/** Route placeholder — the real registration form is built in task 3.2. */
export function RegisterPage() {
  return (
    <div className="page-container">
      <title>Create an account — MAISON NOIR</title>
      <StatusMessage
        title="Create an account"
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
