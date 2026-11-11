import { isRouteErrorResponse, Link, useRouteError } from 'react-router'
import { StatusMessage } from '../components/ui/StatusMessage'

/**
 * Last-resort screen for unexpected errors thrown while rendering a route.
 * Rendered without the normal layout, because the layout itself may have failed.
 */
export function RouteErrorPage() {
  const error = useRouteError()

  if (import.meta.env.DEV) {
    console.error(error)
  }

  const title = isRouteErrorResponse(error) && error.status === 404 ? 'Page not found' : 'Something went wrong'

  return (
    <div className="page-container">
      <StatusMessage
        role="alert"
        title={title}
        action={
          <Link to="/" className="btn-primary">
            Return home
          </Link>
        }
      >
        Please try again in a moment.
      </StatusMessage>
    </div>
  )
}
