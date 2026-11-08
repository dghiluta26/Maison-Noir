import { Link } from 'react-router'
import { StatusMessage } from '../components/ui/StatusMessage'

export function NotFoundPage() {
  return (
    <div className="page-container">
      <title>Page not found — MAISON NOIR</title>
      <StatusMessage
        title="Page not found"
        action={
          <Link to="/" className="btn-primary">
            Return home
          </Link>
        }
      >
        The page you are looking for does not exist or has moved.
      </StatusMessage>
    </div>
  )
}
