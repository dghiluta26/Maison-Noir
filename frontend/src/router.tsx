import { createBrowserRouter } from 'react-router'
import { Layout } from './components/layout/Layout'
import { LoginPage } from './pages/auth/LoginPage'
import { RegisterPage } from './pages/auth/RegisterPage'
import { CataloguePage } from './pages/CataloguePage'
import { HomePage } from './pages/HomePage'
import { NotFoundPage } from './pages/NotFoundPage'
import { ProductDetailPage } from './pages/ProductDetailPage'
import { RouteErrorPage } from './pages/RouteErrorPage'

export const router = createBrowserRouter([
  {
    path: '/',
    Component: Layout,
    ErrorBoundary: RouteErrorPage,
    children: [
      { index: true, Component: HomePage },
      { path: 'products', Component: CataloguePage },
      { path: 'products/:slug', Component: ProductDetailPage },
      { path: 'login', Component: LoginPage },
      { path: 'register', Component: RegisterPage },
      { path: '*', Component: NotFoundPage },
    ],
  },
])
